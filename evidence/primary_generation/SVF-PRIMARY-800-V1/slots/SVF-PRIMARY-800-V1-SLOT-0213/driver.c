#include <curl/curl.h>
#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>

static size_t write_cb(char *ptr, size_t size, size_t nmemb, void *userdata) {
    (void)ptr;
    (void)userdata;
    return size * nmemb;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) {
        return 0;
    }

    CURL *curl = curl_easy_init();
    if (!curl) {
        return 0;
    }

    /* Use input to construct a local file URL, bounded to avoid huge strings. */
    size_t url_len = size < 256 ? size : 256;
    char *url = (char *)malloc(url_len + 1);
    if (!url) {
        curl_easy_cleanup(curl);
        return 0;
    }
    memcpy(url, data, url_len);
    url[url_len] = '\0';

    /* Ensure the URL starts with file:// to keep it local. */
    if (strncmp(url, "file://", 7) != 0) {
        free(url);
        curl_easy_cleanup(curl);
        return 0;
    }

    curl_easy_setopt(curl, CURLOPT_URL, url);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_cb);
    curl_easy_setopt(curl, CURLOPT_NOSIGNAL, 1L);
    curl_easy_setopt(curl, CURLOPT_CONNECTTIMEOUT_MS, 1000L);
    curl_easy_setopt(curl, CURLOPT_TIMEOUT_MS, 1000L);

    /* Use one byte from input to optionally set a follow-location flag. */
    if (data[0] & 1) {
        curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);
    }

    curl_easy_perform(curl);

    curl_easy_cleanup(curl);
    free(url);
    return 0;
}