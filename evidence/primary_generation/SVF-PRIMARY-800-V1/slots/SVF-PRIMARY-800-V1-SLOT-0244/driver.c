#include <curl/curl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

    CURL *curl = curl_easy_init();
    if (!curl) return 0;

    char *path = (char *)malloc(size + 1);
    if (!path) {
        curl_easy_cleanup(curl);
        return 0;
    }
    memcpy(path, data, size);
    path[size] = '\0';

    char url[1024];
    snprintf(url, sizeof(url), "file://%s", path);

    curl_easy_setopt(curl, CURLOPT_URL, url);
    curl_easy_setopt(curl, CURLOPT_TIMEOUT, 1L);
    curl_easy_perform(curl);

    curl_easy_reset(curl);

    curl_easy_setopt(curl, CURLOPT_URL, url);
    curl_easy_setopt(curl, CURLOPT_VERBOSE, 0L);
    curl_easy_perform(curl);

    free(path);
    curl_easy_cleanup(curl);

    return 0;
}