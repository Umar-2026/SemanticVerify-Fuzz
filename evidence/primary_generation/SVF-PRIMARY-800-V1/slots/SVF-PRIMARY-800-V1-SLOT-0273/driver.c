#include <stdio.h>
#include <stdlib.h>
#include <string.h>
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

    // Use the first byte to determine the file path length (bounded)
    size_t path_len = data[0] % 64;
    if (path_len > size - 1) {
        path_len = size - 1;
    }

    // Construct a local file:// URL from the fuzz input
    char url[128];
    snprintf(url, sizeof(url), "file://");
    size_t url_len = strlen(url);
    size_t copy_len = path_len;
    if (url_len + copy_len >= sizeof(url)) {
        copy_len = sizeof(url) - url_len - 1;
    }
    memcpy(url + url_len, data + 1, copy_len);
    url[url_len + copy_len] = '\0';

    CURL *easy = curl_easy_init();
    if (!easy) {
        return 0;
    }

    CURLM *multi = curl_multi_init();
    if (!multi) {
        curl_easy_cleanup(easy);
        return 0;
    }

    curl_easy_setopt(easy, CURLOPT_URL, url);
    curl_easy_setopt(easy, CURLOPT_WRITEFUNCTION, write_callback);
    curl_easy_setopt(easy, CURLOPT_FOLLOWLOCATION, 1L);
    curl_easy_setopt(easy, CURLOPT_MAXREDIRS, 3L);
    curl_easy_setopt(easy, CURLOPT_TIMEOUT_MS, 100L);
    curl_easy_setopt(easy, CURLOPT_CONNECTTIMEOUT_MS, 100L);

    CURLMcode mc = curl_multi_add_handle(multi, easy);
    if (mc != CURLM_OK) {
        curl_multi_cleanup(multi);
        curl_easy_cleanup(easy);
        return 0;
    }

    int still_running = 0;
    int max_iterations = 10;
    do {
        mc = curl_multi_perform(multi, &still_running);
        if (mc != CURLM_OK) {
            break;
        }
        if (still_running) {
            struct timeval timeout;
            timeout.tv_sec = 0;
            timeout.tv_usec = 1000;
            fd_set fdread, fdwrite, fdexcep;
            FD_ZERO(&fdread);
            FD_ZERO(&fdwrite);
            FD_ZERO(&fdexcep);
            int maxfd = -1;
            curl_multi_fdset(multi, &fdread, &fdwrite, &fdexcep, &maxfd);
            if (maxfd >= 0) {
                select(maxfd + 1, &fdread, &fdwrite, &fdexcep, &timeout);
            } else {
                // No file descriptors, just wait a bit
                usleep(1000);
            }
        }
        max_iterations--;
    } while (still_running && max_iterations > 0);

    curl_multi_remove_handle(multi, easy);
    curl_multi_cleanup(multi);
    curl_easy_cleanup(easy);

    return 0;
}