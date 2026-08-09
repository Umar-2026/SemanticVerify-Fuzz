#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>

static size_t write_cb(char *ptr, size_t size, size_t nmemb, void *userdata) {
    size_t total = size * nmemb;
    unsigned char *buf = (unsigned char *)userdata;
    /* The buffer is 4096 bytes, we just ignore overflow for fuzzing */
    if (total > 4096) total = 4096;
    memcpy(buf, ptr, total);
    return total;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    CURL *curl = NULL;
    CURLcode res;
    char url[128];
    unsigned char outbuf[4096];
    size_t i;

    if (size < 1) return 0;

    /* Initialize libcurl */
    if (curl_global_init(CURL_GLOBAL_DEFAULT) != CURLE_OK) {
        return 0;
    }

    curl = curl_easy_init();
    if (!curl) {
        curl_global_cleanup();
        return 0;
    }

    /* Build a local file URL from fuzz data (bounded) */
    snprintf(url, sizeof(url), "file:///tmp/fuzz_%u", (unsigned)data[0]);
    for (i = 1; i < size && i < 100; i++) {
        /* Use some bytes to vary the path, but keep it simple */
        if (data[i] == '\0') break;
        /* We just append a hex char to the filename */
        snprintf(url + strlen(url), sizeof(url) - strlen(url), "%02x", data[i]);
    }

    /* Set options */
    curl_easy_setopt(curl, CURLOPT_URL, url);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_cb);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, outbuf);
    curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 0L);
    curl_easy_setopt(curl, CURLOPT_TIMEOUT_MS, 1000L);

    /* Perform the transfer */
    res = curl_easy_perform(curl);

    /* Cleanup */
    curl_easy_cleanup(curl);
    curl_global_cleanup();

    return 0;
}