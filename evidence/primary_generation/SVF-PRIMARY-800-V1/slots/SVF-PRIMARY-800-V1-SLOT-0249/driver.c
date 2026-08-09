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
    if (size < 2) {
        return 0;
    }

    CURL *h = curl_easy_init();
    if (!h) {
        return 0;
    }

    // First operation: use first half of input as file path (NUL-terminated)
    size_t first_len = size / 2;
    char *path1 = (char *)malloc(first_len + 1);
    if (!path1) {
        curl_easy_cleanup(h);
        return 0;
    }
    memcpy(path1, data, first_len);
    path1[first_len] = '\0';

    // Second operation: use second half of input as file path
    size_t second_len = size - first_len;
    char *path2 = (char *)malloc(second_len + 1);
    if (!path2) {
        free(path1);
        curl_easy_cleanup(h);
        return 0;
    }
    memcpy(path2, data + first_len, second_len);
    path2[second_len] = '\0';

    // Configure first operation
    curl_easy_setopt(h, CURLOPT_URL, path1);
    curl_easy_setopt(h, CURLOPT_WRITEFUNCTION, discard_write);
    curl_easy_setopt(h, CURLOPT_NOSIGNAL, 1L);
    curl_easy_setopt(h, CURLOPT_FOLLOWLOCATION, 0L);

    // Perform first operation
    CURLcode res = curl_easy_perform(h);
    (void)res;

    // Reset handle for second independent configuration
    curl_easy_reset(h);

    // Configure second operation
    curl_easy_setopt(h, CURLOPT_URL, path2);
    curl_easy_setopt(h, CURLOPT_WRITEFUNCTION, discard_write);
    curl_easy_setopt(h, CURLOPT_NOSIGNAL, 1L);
    curl_easy_setopt(h, CURLOPT_FOLLOWLOCATION, 0L);

    // Perform second operation
    res = curl_easy_perform(h);
    (void)res;

    free(path1);
    free(path2);
    curl_easy_cleanup(h);

    return 0;
}