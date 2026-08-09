#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include "curl/curl.h"

static size_t write_callback(char *ptr, size_t size, size_t nmemb, void *userdata) {
    size_t total = size * nmemb;
    char **buf = (char **)userdata;
    size_t cur_len = *buf ? strlen(*buf) : 0;
    char *new_buf = realloc(*buf, cur_len + total + 1);
    if (!new_buf) {
        return 0;
    }
    *buf = new_buf;
    memcpy(*buf + cur_len, ptr, total);
    (*buf)[cur_len + total] = '\0';
    return total;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1) {
        return 0;
    }

    // Bounded configuration from fuzz input
    uint8_t opt_byte = data[0];
    size_t remaining = size - 1;
    const uint8_t *payload = data + 1;

    // Limit payload size to avoid excessive memory usage
    if (remaining > 4096) {
        remaining = 4096;
    }

    // Build a local file URL with a fixed path (no external access)
    char url[] = "file:///tmp/curl_fuzz_input";
    FILE *fp = fopen("/tmp/curl_fuzz_input", "wb");
    if (!fp) {
        return 0;
    }
    fwrite(payload, 1, remaining, fp);
    fclose(fp);

    // Initialize libcurl
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

    // Set URL
    curl_easy_setopt(curl, CURLOPT_URL, url);

    // Set write callback to capture output
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &output);

    // Bounded fuzz-derived configuration
    switch (opt_byte % 4) {
        case 0:
            // Follow redirects (disabled for file://, but set anyway)
            curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);
            break;
        case 1:
            // Set a timeout
            curl_easy_setopt(curl, CURLOPT_TIMEOUT, 5L);
            break;
        case 2:
            // Set user agent
            curl_easy_setopt(curl, CURLOPT_USERAGENT, "fuzz-agent");
            break;
        case 3:
            // Set no signal
            curl_easy_setopt(curl, CURLOPT_NOSIGNAL, 1L);
            break;
        default:
            break;
    }

    // Perform the transfer
    CURLcode res = curl_easy_perform(curl);

    // Cleanup
    curl_easy_cleanup(curl);
    curl_global_cleanup();

    if (output) {
        free(output);
    }

    // Remove temporary file
    remove("/tmp/curl_fuzz_input");

    return 0;
}