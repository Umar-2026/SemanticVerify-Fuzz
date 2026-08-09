#include <curl/curl.h>
#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <stdlib.h>

static size_t write_callback(char *ptr, size_t size, size_t nmemb, void *userdata) {
    (void)ptr;
    (void)userdata;
    return size * nmemb;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1) {
        return 0;
    }

    CURL *curl = curl_easy_init();
    if (!curl) {
        return 0;
    }

    // Use input to derive a local file path (bounded, simple)
    // We'll construct a path like "file:///tmp/fuzz_XXXX" where XXXX comes from input
    char path[64];
    uint32_t seed = 0;
    if (size >= 4) {
        seed = (uint32_t)data[0] | ((uint32_t)data[1] << 8) | ((uint32_t)data[2] << 16) | ((uint32_t)data[3] << 24);
    } else {
        seed = (uint32_t)data[0];
    }
    snprintf(path, sizeof(path), "file:///tmp/fuzz_%08x", seed);

    // Set URL
    curl_easy_setopt(curl, CURLOPT_URL, path);

    // Use output callback to discard data
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);

    // Optionally set a timeout based on input to bound execution
    long timeout = 1 + (data[0] % 10); // 1-10 seconds
    curl_easy_setopt(curl, CURLOPT_TIMEOUT, timeout);

    // Perform the transfer
    CURLcode res = curl_easy_perform(curl);
    (void)res;

    curl_easy_cleanup(curl);
    return 0;
}