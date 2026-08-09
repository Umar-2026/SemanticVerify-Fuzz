#include <stddef.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>

static size_t write_cb(char *ptr, size_t size, size_t nmemb, void *userdata) {
    (void)ptr;
    (void)userdata;
    return size * nmemb;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1) {
        return 0;
    }

    CURLM *multi = curl_multi_init();
    if (!multi) {
        return 0;
    }

    CURL *easy = curl_easy_init();
    if (!easy) {
        curl_multi_cleanup(multi);
        return 0;
    }

    char url[256];
    size_t len = size < sizeof(url) - 1 ? size : sizeof(url) - 1;
    memcpy(url, data, len);
    url[len] = '\0';

    curl_easy_setopt(easy, CURLOPT_URL, url);
    curl_easy_setopt(easy, CURLOPT_WRITEFUNCTION, write_cb);
    curl_easy_setopt(easy, CURLOPT_FOLLOWLOCATION, 0L);
    curl_easy_setopt(easy, CURLOPT_MAXREDIRS, 0L);
    curl_easy_setopt(easy, CURLOPT_TIMEOUT_MS, 1000L);
    curl_easy_setopt(easy, CURLOPT_CONNECTTIMEOUT_MS, 500L);
    curl_easy_setopt(easy, CURLOPT_NOSIGNAL, 1L);

    CURLMcode mc = curl_multi_add_handle(multi, easy);
    if (mc != CURLM_OK) {
        curl_easy_cleanup(easy);
        curl_multi_cleanup(multi);
        return 0;
    }

    int running = 1;
    int loops = 0;
    while (running && loops < 100) {
        mc = curl_multi_perform(multi, &running);
        if (mc != CURLM_OK) {
            break;
        }
        if (running) {
            struct timeval tv;
            tv.tv_sec = 0;
            tv.tv_usec = 1000;
            fd_set fdread, fdwrite, fdexcep;
            FD_ZERO(&fdread);
            FD_ZERO(&fdwrite);
            FD_ZERO(&fdexcep);
            int maxfd = -1;
            mc = curl_multi_fdset(multi, &fdread, &fdwrite, &fdexcep, &maxfd);
            if (mc != CURLM_OK) {
                break;
            }
            if (maxfd == -1) {
                continue;
            }
            select(maxfd + 1, &fdread, &fdwrite, &fdexcep, &tv);
        }
        loops++;
    }

    curl_multi_remove_handle(multi, easy);
    curl_easy_cleanup(easy);
    curl_multi_cleanup(multi);
    return 0;
}