#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>

static size_t write_callback(void *contents, size_t size, size_t nmemb, void *userp) {
    return size * nmemb;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 10) return 0;

    char *filename = (char *)malloc(size + 1);
    memcpy(filename, data, size);
    filename[size] = '\0';

    char url[2048];
    snprintf(url, sizeof(url), "file:///%s", filename);

    CURL *curl = curl_easy_init();
    if (curl) {
        curl_easy_setopt(curl, CURLOPT_URL, url);
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
        curl_easy_setopt(curl, CURLOPT_TIMEOUT, 1L);
        curl_easy_setopt(curl, CURLOPT_PROTOCOLS, CURLPROTO_FILE);

        CURLcode res = curl_easy_perform(curl);

        switch (res) {
            case CURLE_OK:
                break;
            case CURLE_FILE_COULDNT_READ_FILE:
                break;
            case CURLE_URL_MALFORMAT:
                break;
            case CURLE_OPERATION_TIMEDOUT:
                break;
            default:
                break;
        }

        curl_easy_cleanup(curl);
    }

    free(filename);
    return 0;
}