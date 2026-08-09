#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <curl/curl.h>

static size_t write_cb(char *ptr, size_t size, size_t nmemb, void *userdata) {
    (void)ptr;
    (void)userdata;
    return size * nmemb;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1) return 0;

    // Create a temporary file with fuzz-controlled content
    char path[] = "/tmp/curl_fuzz_XXXXXX";
    int fd = mkstemp(path);
    if (fd < 0) return 0;
    write(fd, data, size);
    close(fd);

    // Build file:// URL from the temp path
    char url[512];
    snprintf(url, sizeof(url), "file://%s", path);

    CURL *easy = curl_easy_init();
    CURLM *multi = curl_multi_init();
    if (!easy || !multi) {
        if (easy) curl_easy_cleanup(easy);
        if (multi) curl_multi_cleanup(multi);
        unlink(path);
        return 0;
    }

    curl_easy_setopt(easy, CURLOPT_URL, url);
    curl_easy_setopt(easy, CURLOPT_WRITEFUNCTION, write_cb);
    curl_easy_setopt(easy, CURLOPT_NOSIGNAL, 1L);
    curl_easy_setopt(easy, CURLOPT_CONNECTTIMEOUT_MS, 1000L);
    curl_easy_setopt(easy, CURLOPT_TIMEOUT_MS, 2000L);

    CURLMcode mc = curl_multi_add_handle(multi, easy);
    if (mc != CURLM_OK) {
        curl_easy_cleanup(easy);
        curl_multi_cleanup(multi);
        unlink(path);
        return 0;
    }

    int still_running = 0;
    do {
        mc = curl_multi_perform(multi, &still_running);
        if (mc != CURLM_OK) break;
        if (still_running) {
            struct timeval timeout;
            fd_set fdread, fdwrite, fdexcep;
            int maxfd = -1;
            FD_ZERO(&fdread);
            FD_ZERO(&fdwrite);
            FD_ZERO(&fdexcep);
            timeout.tv_sec = 0;
            timeout.tv_usec = 10000;
            curl_multi_fdset(multi, &fdread, &fdwrite, &fdexcep, &maxfd);
            select(maxfd + 1, &fdread, &fdwrite, &fdexcep, &timeout);
        }
    } while (still_running);

    curl_multi_remove_handle(multi, easy);
    curl_easy_cleanup(easy);
    curl_multi_cleanup(multi);
    unlink(path);
    return 0;
}