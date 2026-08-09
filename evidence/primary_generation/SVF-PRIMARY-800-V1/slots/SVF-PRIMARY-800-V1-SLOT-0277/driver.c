#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <curl/curl.h>

static size_t write_callback(char *ptr, size_t size, size_t nmemb, void *userdata) {
    (void)ptr;
    (void)userdata;
    return size * nmemb;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1) {
        return 0;
    }

    // Use first byte to determine file size (bounded to 1KB)
    size_t file_size = (data[0] % 1024) + 1;
    if (size < file_size + 1) {
        file_size = size - 1;
    }

    // Create a temporary file with fuzz data
    char tmp_path[] = "/tmp/curl_fuzz_XXXXXX";
    int fd = mkstemp(tmp_path);
    if (fd == -1) {
        return 0;
    }
    ssize_t written = write(fd, data + 1, file_size);
    if (written != (ssize_t)file_size) {
        close(fd);
        unlink(tmp_path);
        return 0;
    }
    close(fd);

    // Build file:// URL
    char url[512];
    snprintf(url, sizeof(url), "file://%s", tmp_path);

    CURLM *multi = curl_multi_init();
    CURL *easy = curl_easy_init();
    if (!multi || !easy) {
        if (multi) curl_multi_cleanup(multi);
        if (easy) curl_easy_cleanup(easy);
        unlink(tmp_path);
        return 0;
    }

    curl_easy_setopt(easy, CURLOPT_URL, url);
    curl_easy_setopt(easy, CURLOPT_WRITEFUNCTION, write_callback);
    curl_easy_setopt(easy, CURLOPT_NOSIGNAL, 1L);
    curl_easy_setopt(easy, CURLOPT_CONNECTTIMEOUT_MS, 1000L);
    curl_easy_setopt(easy, CURLOPT_TIMEOUT_MS, 1000L);

    CURLMcode mc = curl_multi_add_handle(multi, easy);
    if (mc != CURLM_OK) {
        curl_easy_cleanup(easy);
        curl_multi_cleanup(multi);
        unlink(tmp_path);
        return 0;
    }

    int still_running = 0;
    int max_iterations = 100;
    do {
        mc = curl_multi_perform(multi, &still_running);
        if (mc != CURLM_OK) {
            break;
        }
        if (still_running) {
            struct timeval timeout;
            fd_set fdread, fdwrite, fdexcep;
            int maxfd = -1;
            FD_ZERO(&fdread);
            FD_ZERO(&fdwrite);
            FD_ZERO(&fdexcep);
            timeout.tv_sec = 0;
            timeout.tv_usec = 1000;
            curl_multi_fdset(multi, &fdread, &fdwrite, &fdexcep, &maxfd);
            select(maxfd + 1, &fdread, &fdwrite, &fdexcep, &timeout);
        }
    } while (still_running && --max_iterations > 0);

    curl_multi_remove_handle(multi, easy);
    curl_easy_cleanup(easy);
    curl_multi_cleanup(multi);
    unlink(tmp_path);

    return 0;
}