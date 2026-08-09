#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <curl/curl.h>

static size_t write_callback(char *ptr, size_t size, size_t nmemb, void *userdata) {
    size_t total = size * nmemb;
    char **buf = (char **)userdata;
    size_t current_len = *buf ? strlen(*buf) : 0;
    char *new_buf = realloc(*buf, current_len + total + 1);
    if (!new_buf) {
        return 0;
    }
    *buf = new_buf;
    memcpy(*buf + current_len, ptr, total);
    (*buf)[current_len + total] = '\0';
    return total;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) {
        return 0;
    }

    // Bounded configuration from fuzz input
    uint8_t timeout = data[0];
    uint8_t follow_redirects = data[1] & 0x01;
    uint8_t verbose = (data[1] >> 1) & 0x01;
    uint8_t ssl_verify = (data[1] >> 2) & 0x01;

    // Use a fixed local file URL
    const char *url = "file:///tmp/curl_fuzz_input.txt";

    // Initialize libcurl globally
    if (curl_global_init(CURL_GLOBAL_DEFAULT) != CURLE_OK) {
        return 0;
    }

    CURL *curl = curl_easy_init();
    if (!curl) {
        curl_global_cleanup();
        return 0;
    }

    // Application output buffer
    char *output = NULL;

    // Set options with bounded values
    curl_easy_setopt(curl, CURLOPT_URL, url);
    curl_easy_setopt(curl, CURLOPT_TIMEOUT, (long)timeout);
    curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, follow_redirects ? 1L : 0L);
    curl_easy_setopt(curl, CURLOPT_VERBOSE, verbose ? 1L : 0L);
    curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, ssl_verify ? 1L : 0L);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &output);

    // Perform the transfer
    CURLcode res = curl_easy_perform(curl);

    // Cleanup
    if (output) {
        free(output);
    }
    curl_easy_cleanup(curl);
    curl_global_cleanup();

    return 0;
}