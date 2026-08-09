#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>

static size_t write_callback(char *ptr, size_t size, size_t nmemb, void *userdata) {
    (void)ptr;
    (void)userdata;
    return size * nmemb;
}

int LLVMFuzzerTestOneInput(const unsigned char *data, size_t size) {
    if (size < 1) {
        return 0;
    }

    CURL *curl = curl_easy_init();
    if (!curl) {
        return 0;
    }

    char url[256];
    size_t len = size < sizeof(url) - 1 ? size : sizeof(url) - 1;
    memcpy(url, data, len);
    url[len] = '\0';

    curl_easy_setopt(curl, CURLOPT_URL, url);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
    curl_easy_setopt(curl, CURLOPT_NOSIGNAL, 1L);
    curl_easy_setopt(curl, CURLOPT_CONNECTTIMEOUT_MS, 100L);
    curl_easy_setopt(curl, CURLOPT_TIMEOUT_MS, 100L);
    curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 0L);
    curl_easy_setopt(curl, CURLOPT_MAXREDIRS, 0L);

    CURLcode res = curl_easy_perform(curl);

    switch (res) {
        case CURLE_OK:
            break;
        case CURLE_UNSUPPORTED_PROTOCOL:
            break;
        case CURLE_URL_MALFORMAT:
            break;
        case CURLE_COULDNT_RESOLVE_HOST:
            break;
        case CURLE_COULDNT_CONNECT:
            break;
        case CURLE_OPERATION_TIMEDOUT:
            break;
        case CURLE_FILE_COULDNT_READ_FILE:
            break;
        default:
            break;
    }

    curl_easy_cleanup(curl);
    return 0;
}