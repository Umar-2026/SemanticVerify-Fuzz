#include <curl/curl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1) {
        return 0;
    }

    CURL *curl = curl_easy_init();
    if (!curl) {
        return 0;
    }

    char *filename = (char *)malloc(size + 1);
    if (!filename) {
        curl_easy_cleanup(curl);
        return 0;
    }
    memcpy(filename, data, size);
    filename[size] = '\0';

    char url[1024];
    snprintf(url, sizeof(url), "file://%s", filename);

    curl_easy_setopt(curl, CURLOPT_URL, url);
    curl_easy_setopt(curl, CURLOPT_TIMEOUT, 1L);
    curl_easy_setopt(curl, CURLOPT_NOPROGRESS, 1L);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, stdout);

    curl_easy_perform(curl);

    curl_easy_cleanup(curl);
    free(filename);

    return 0;
}