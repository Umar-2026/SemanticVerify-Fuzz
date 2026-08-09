#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>

static size_t write_callback(char *ptr, size_t size, size_t nmemb, void *userdata) {
    (void)ptr;
    (void)userdata;
    return size * nmemb;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) {
        return 0;
    }

    // Split input into two parts for two file paths
    size_t split = (size_t)data[0] % (size - 1) + 1;
    const uint8_t *path1_data = data + 1;
    size_t path1_len = split;
    const uint8_t *path2_data = data + 1 + split;
    size_t path2_len = size - 1 - split;

    if (path1_len == 0 || path2_len == 0) {
        return 0;
    }

    // Construct file URLs from the input bytes (treat as raw path, but ensure no NUL)
    char url1[256];
    char url2[256];
    if (path1_len >= sizeof(url1) - 6 || path2_len >= sizeof(url2) - 6) {
        return 0;
    }

    memcpy(url1, "file://", 7);
    memcpy(url1 + 7, path1_data, path1_len);
    url1[7 + path1_len] = '\0';

    memcpy(url2, "file://", 7);
    memcpy(url2 + 7, path2_data, path2_len);
    url2[7 + path2_len] = '\0';

    CURL *curl = curl_easy_init();
    if (!curl) {
        return 0;
    }

    // First operation
    curl_easy_setopt(curl, CURLOPT_URL, url1);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
    curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 0L);
    curl_easy_setopt(curl, CURLOPT_NOSIGNAL, 1L);
    curl_easy_perform(curl);

    // Reset handle
    curl_easy_reset(curl);

    // Second operation with different URL and options
    curl_easy_setopt(curl, CURLOPT_URL, url2);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
    curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);
    curl_easy_setopt(curl, CURLOPT_NOSIGNAL, 1L);
    curl_easy_perform(curl);

    curl_easy_cleanup(curl);
    return 0;
}