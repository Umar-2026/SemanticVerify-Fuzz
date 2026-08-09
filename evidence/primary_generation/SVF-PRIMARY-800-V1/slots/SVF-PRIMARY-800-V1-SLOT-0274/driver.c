#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 10) return 0;

    char filename[256];
    size_t name_len = (size - 1 < 255) ? size - 1 : 255;
    memcpy(filename, data, name_len);
    filename[name_len] = '\0';

    char url[512];
    snprintf(url, sizeof(url), "file:///%s", filename);

    CURLM *multi_handle = curl_multi_init();
    CURL *easy_handle = curl_easy_init();

    if (multi_handle && easy_handle) {
        curl_easy_setopt(easy_handle, CURLOPT_URL, url);
        curl_easy_setopt(easy_handle, CURLOPT_TIMEOUT, 1L);
        curl_easy_setopt(easy_handle, CURLOPT_NOPROGRESS, 1L);

        curl_multi_add_handle(multi_handle, easy_handle);

        int still_running;
        curl_multi_perform(multi_handle, &still_running);

        curl_multi_remove_handle(multi_handle, easy_handle);
    }

    if (easy_handle) {
        curl_easy_cleanup(easy_handle);
    }
    if (multi_handle) {
        curl_multi_cleanup(multi_handle);
    }

    return 0;
}