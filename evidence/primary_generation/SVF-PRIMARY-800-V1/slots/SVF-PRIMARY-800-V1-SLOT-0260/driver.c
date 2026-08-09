#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>

static size_t write_callback(char *ptr, size_t size, size_t nmemb, void *userdata) {
    return size * nmemb;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 10) return 0;

    char *filename = malloc(size + 1);
    if (!filename) return 0;
    memcpy(filename, data, size);
    filename[size] = '\0';

    CURL *curl = curl_easy_init();
    if (curl) {
        char url[1024];
        snprintf(url, sizeof(url), "file://%s", filename);

        curl_easy_setopt(curl, CURLOPT_URL, url);
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
        curl_easy_setopt(curl, CURLOPT_TIMEOUT, 1L);
        curl_easy_setopt(curl, CURLOPT_NOSIGNAL, 1L);

        curl_easy_perform(curl);
        curl_easy_cleanup(curl);
    }

    free(filename);
    return 0;
}