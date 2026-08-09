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

    // Split input into two file paths (null-terminated within the input)
    size_t first_len = 0;
    while (first_len < size && data[first_len] != '\0') {
        first_len++;
    }
    if (first_len == size) {
        return 0;
    }
    size_t second_len = size - first_len - 1;
    if (second_len == 0) {
        return 0;
    }

    char *path1 = (char *)malloc(first_len + 1);
    char *path2 = (char *)malloc(second_len + 1);
    if (!path1 || !path2) {
        free(path1);
        free(path2);
        return 0;
    }
    memcpy(path1, data, first_len);
    path1[first_len] = '\0';
    memcpy(path2, data + first_len + 1, second_len);
    path2[second_len] = '\0';

    CURL *curl = curl_easy_init();
    if (!curl) {
        free(path1);
        free(path2);
        return 0;
    }

    char url1[4096];
    char url2[4096];
    snprintf(url1, sizeof(url1), "file://%s", path1);
    snprintf(url2, sizeof(url2), "file://%s", path2);

    // First operation
    curl_easy_setopt(curl, CURLOPT_URL, url1);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, discard_write);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, NULL);
    curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 0L);
    curl_easy_perform(curl);

    // Reset handle and configure second operation
    curl_easy_reset(curl);
    curl_easy_setopt(curl, CURLOPT_URL, url2);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, discard_write);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, NULL);
    curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);
    curl_easy_perform(curl);

    curl_easy_cleanup(curl);
    free(path1);
    free(path2);
    return 0;
}