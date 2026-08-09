#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>

static size_t write_callback(void *contents, size_t size, size_t nmemb, void *userp) {
    return size * nmemb;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 10 || size > 2048) {
        return 0;
    }

    char *url = malloc(size + 8);
    if (!url) return 0;

    memcpy(url, "file://", 7);
    memcpy(url + 7, data, size);
    url[size + 7] = '\0';

    CURL *curl = curl_easy_init();
    if (curl) {
        curl_easy_setopt(curl, CURLOPT_URL, url);
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
        curl_easy_setopt(curl, CURLOPT_TIMEOUT, 1L);
        curl_easy_setopt(curl, CURLOPT_NOSIGNAL, 1L);

        curl_easy_perform(curl);
        curl_easy_cleanup(curl);
    }

    free(url);
    return 0;
}