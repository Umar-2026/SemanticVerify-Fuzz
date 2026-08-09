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

    CURLM *multi_handle = curl_multi_init();
    if (!multi_handle) {
        return 0;
    }

    CURL *easy_handle = curl_easy_init();
    if (!easy_handle) {
        curl_multi_cleanup(multi_handle);
        return 0;
    }

    char url[256];
    snprintf(url, sizeof(url), "file:///tmp/fuzz_%08x", (unsigned int)data[0]);

    curl_easy_setopt(easy_handle, CURLOPT_URL, url);
    curl_easy_setopt(easy_handle, CURLOPT_WRITEFUNCTION, write_callback);
    curl_easy_setopt(easy_handle, CURLOPT_TIMEOUT_MS, 100L);
    curl_easy_setopt(easy_handle, CURLOPT_CONNECTTIMEOUT_MS, 100L);
    curl_easy_setopt(easy_handle, CURLOPT_NOSIGNAL, 1L);

    CURLMcode mc = curl_multi_add_handle(multi_handle, easy_handle);
    if (mc != CURLM_OK) {
        curl_easy_cleanup(easy_handle);
        curl_multi_cleanup(multi_handle);
        return 0;
    }

    int still_running = 0;
    int max_iterations = 100;
    do {
        mc = curl_multi_perform(multi_handle, &still_running);
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
            curl_multi_fdset(multi_handle, &fdread, &fdwrite, &fdexcep, &maxfd);
            if (maxfd >= 0) {
                select(maxfd + 1, &fdread, &fdwrite, &fdexcep, &timeout);
            } else {
                usleep(1000);
            }
        }
    } while (still_running && --max_iterations > 0);

    curl_multi_remove_handle(multi_handle, easy_handle);
    curl_easy_cleanup(easy_handle);
    curl_multi_cleanup(multi_handle);

    return 0;
}