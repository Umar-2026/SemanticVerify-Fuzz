#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>

static size_t discard_write(void *ptr, size_t size, size_t nmemb, void *userdata) {
    (void)ptr;
    (void)userdata;
    return size * nmemb;
}

int LLVMFuzzerTestOneInput(const unsigned char *data, size_t size) {
    CURL *curl;
    CURLcode res;
    char url[256];
    size_t len = size;
    if (len > sizeof(url) - 1) {
        len = sizeof(url) - 1;
    }
    memcpy(url, data, len);
    url[len] = '\0';

    curl = curl_easy_init();
    if (!curl) {
        return 0;
    }

    curl_easy_setopt(curl, CURLOPT_URL, url);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, discard_write);
    curl_easy_setopt(curl, CURLOPT_TIMEOUT, 2L);
    curl_easy_setopt(curl, CURLOPT_CONNECTTIMEOUT, 2L);
    curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 0L);
    curl_easy_setopt(curl, CURLOPT_PROTOCOLS, CURLPROTO_FILE);
    curl_easy_setopt(curl, CURLOPT_REDIR_PROTOCOLS, 0L);

    res = curl_easy_perform(curl);

    switch (res) {
        case CURLE_OK:
            break;
        case CURLE_UNSUPPORTED_PROTOCOL:
            break;
        case CURLE_COULDNT_RESOLVE_HOST:
            break;
        case CURLE_COULDNT_CONNECT:
            break;
        case CURLE_FILE_COULDNT_READ_FILE:
            break;
        case CURLE_OPERATION_TIMEDOUT:
            break;
        default:
            break;
    }

    curl_easy_cleanup(curl);
    return 0;
}