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

    // Use input to derive a local file path (bounded, no path traversal)
    char path[64];
    size_t path_len = size < sizeof(path) - 1 ? size : sizeof(path) - 1;
    memcpy(path, data, path_len);
    path[path_len] = '\0';

    // Ensure it's a file:// URL
    char url[128];
    snprintf(url, sizeof(url), "file://%s", path);

    curl_easy_setopt(curl, CURLOPT_URL, url);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, NULL);
    curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 0L);
    curl_easy_setopt(curl, CURLOPT_CONNECTTIMEOUT_MS, 1000L);
    curl_easy_setopt(curl, CURLOPT_TIMEOUT_MS, 1000L);

    // Use a small portion of input to set a buffer size option if present
    if (size > 1) {
        long buffer_size = (long)(data[1] % 4096) + 1;
        curl_easy_setopt(curl, CURLOPT_BUFFERSIZE, buffer_size);
    }

    curl_easy_perform(curl);

    curl_easy_cleanup(curl);
    return 0;
}