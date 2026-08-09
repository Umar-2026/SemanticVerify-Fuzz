#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <curl/curl.h>

static size_t write_cb(char *ptr, size_t size, size_t nmemb, void *userdata) {
    size_t total = size * nmemb;
    char **buf = (char **)userdata;
    size_t cur_len = *buf ? strlen(*buf) : 0;
    char *newbuf = realloc(*buf, cur_len + total + 1);
    if (!newbuf) return 0;
    memcpy(newbuf + cur_len, ptr, total);
    newbuf[cur_len + total] = '\0';
    *buf = newbuf;
    return total;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 4) return 0;

    // Bounded configuration from fuzz input
    long timeout_ms = 1 + (data[0] % 1000);
    long connect_timeout_ms = 1 + (data[1] % 1000);
    int follow_redirects = data[2] % 2;
    int verbose = data[3] % 2;

    // Local file source: use a fixed path, content is not fuzz-controlled
    const char *url = "file:///tmp/curl_fuzz_input.txt";

    // Application output buffer
    char *output = NULL;

    // Library setup
    if (curl_global_init(CURL_GLOBAL_DEFAULT) != CURLE_OK) {
        return 0;
    }

    CURL *easy = curl_easy_init();
    if (!easy) {
        curl_global_cleanup();
        return 0;
    }

    // Configure easy transfer
    curl_easy_setopt(easy, CURLOPT_URL, url);
    curl_easy_setopt(easy, CURLOPT_TIMEOUT_MS, timeout_ms);
    curl_easy_setopt(easy, CURLOPT_CONNECTTIMEOUT_MS, connect_timeout_ms);
    curl_easy_setopt(easy, CURLOPT_FOLLOWLOCATION, follow_redirects);
    curl_easy_setopt(easy, CURLOPT_VERBOSE, verbose);
    curl_easy_setopt(easy, CURLOPT_WRITEFUNCTION, write_cb);
    curl_easy_setopt(easy, CURLOPT_WRITEDATA, &output);

    // Perform transfer
    CURLcode res = curl_easy_perform(easy);

    // Cleanup
    curl_easy_cleanup(easy);
    curl_global_cleanup();

    if (output) {
        free(output);
    }

    return 0;
}