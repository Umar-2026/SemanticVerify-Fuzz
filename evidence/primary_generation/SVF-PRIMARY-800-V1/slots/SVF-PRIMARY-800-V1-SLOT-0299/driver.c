#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

#include <curl/curl.h>

static size_t write_callback(char *ptr, size_t size, size_t nmemb, void *userdata) {
    size_t total = size * nmemb;
    unsigned char *buf = (unsigned char *)userdata;
    /* buf layout: [4 bytes length][data...] */
    uint32_t *len = (uint32_t *)buf;
    unsigned char *data = buf + 4;
    if (*len + total > 4096) {
        total = 4096 - *len;
    }
    memcpy(data + *len, ptr, total);
    *len += total;
    return total;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 8) return 0;

    /* Bounded configuration from fuzz input */
    uint32_t timeout_ms = 0;
    uint32_t connect_timeout_ms = 0;
    memcpy(&timeout_ms, data, 4);
    memcpy(&connect_timeout_ms, data + 4, 4);
    timeout_ms %= 10000;
    connect_timeout_ms %= 10000;

    /* Use a fixed local file URL */
    const char *url = "file:///tmp/fuzz_input.txt";

    /* Application output buffer: 4-byte length + 4096 data */
    unsigned char outbuf[4100];
    memset(outbuf, 0, sizeof(outbuf));

    /* Library setup */
    if (curl_global_init(CURL_GLOBAL_DEFAULT) != CURLE_OK) {
        return 0;
    }

    CURL *easy = curl_easy_init();
    if (!easy) {
        curl_global_cleanup();
        return 0;
    }

    /* Configure the easy handle */
    curl_easy_setopt(easy, CURLOPT_URL, url);
    curl_easy_setopt(easy, CURLOPT_WRITEFUNCTION, write_callback);
    curl_easy_setopt(easy, CURLOPT_WRITEDATA, outbuf);
    curl_easy_setopt(easy, CURLOPT_TIMEOUT_MS, timeout_ms);
    curl_easy_setopt(easy, CURLOPT_CONNECTTIMEOUT_MS, connect_timeout_ms);
    curl_easy_setopt(easy, CURLOPT_FOLLOWLOCATION, 0L);
    curl_easy_setopt(easy, CURLOPT_NOSIGNAL, 1L);

    /* Perform the transfer */
    curl_easy_perform(easy);

    /* Cleanup */
    curl_easy_cleanup(easy);
    curl_global_cleanup();

    return 0;
}