#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>

static size_t discard_data(void *ptr, size_t size, size_t nmemb, void *userdata) {
    (void)ptr;
    (void)userdata;
    return size * nmemb;
}

int main(int argc, char **argv) {
    CURL *curl;
    CURLcode res;
    char url[256];
    long response_code = 0;

    if (argc != 2) {
        fprintf(stderr, "Usage: %s <file_path>\n", argv[0]);
        return 1;
    }

    snprintf(url, sizeof(url), "file://%s", argv[1]);

    curl_global_init(CURL_GLOBAL_DEFAULT);
    curl = curl_easy_init();
    if (!curl) {
        fprintf(stderr, "Failed to initialize curl\n");
        curl_global_cleanup();
        return 1;
    }

    curl_easy_setopt(curl, CURLOPT_URL, url);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, discard_data);
    curl_easy_setopt(curl, CURLOPT_NOPROGRESS, 1L);
    curl_easy_setopt(curl, CURLOPT_TIMEOUT, 5L);

    res = curl_easy_perform(curl);

    if (res == CURLE_OK) {
        curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &response_code);
        printf("SUCCESS: transfer completed, response code %ld\n", response_code);
    } else if (res == CURLE_FILE_COULDNT_READ_FILE) {
        printf("FILE_NOT_FOUND: could not read file\n");
    } else if (res == CURLE_COULDNT_RESOLVE_HOST) {
        printf("RESOLVE_ERROR: could not resolve host\n");
    } else if (res == CURLE_OPERATION_TIMEDOUT) {
        printf("TIMEOUT: operation timed out\n");
    } else if (res == CURLE_UNSUPPORTED_PROTOCOL) {
        printf("UNSUPPORTED_PROTOCOL: protocol not supported\n");
    } else {
        printf("ERROR: curl code %d (%s)\n", (int)res, curl_easy_strerror(res));
    }

    curl_easy_cleanup(curl);
    curl_global_cleanup();
    return 0;
}