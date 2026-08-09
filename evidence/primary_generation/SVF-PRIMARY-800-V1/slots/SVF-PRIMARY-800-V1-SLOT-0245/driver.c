#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>

static size_t discard_write(void *ptr, size_t size, size_t nmemb, void *userdata) {
    (void)ptr;
    (void)userdata;
    return size * nmemb;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) {
        return 0;
    }

    CURL *curl = curl_easy_init();
    if (!curl) {
        return 0;
    }

    char *url1 = (char *)malloc(size / 2 + 1);
    char *url2 = (char *)malloc(size - size / 2 + 1);
    if (!url1 || !url2) {
        free(url1);
        free(url2);
        curl_easy_cleanup(curl);
        return 0;
    }

    memcpy(url1, data, size / 2);
    url1[size / 2] = '\0';
    memcpy(url2, data + size / 2, size - size / 2);
    url2[size - size / 2] = '\0';

    curl_easy_setopt(curl, CURLOPT_URL, url1);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, discard_write);
    curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);
    curl_easy_setopt(curl, CURLOPT_MAXREDIRS, 5L);
    curl_easy_perform(curl);

    curl_easy_reset(curl);

    curl_easy_setopt(curl, CURLOPT_URL, url2);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, discard_write);
    curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 0L);
    curl_easy_setopt(curl, CURLOPT_TIMEOUT, 10L);
    curl_easy_perform(curl);

    free(url1);
    free(url2);
    curl_easy_cleanup(curl);
    return 0;
}