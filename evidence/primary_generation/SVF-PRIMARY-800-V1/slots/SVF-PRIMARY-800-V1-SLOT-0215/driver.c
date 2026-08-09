#include <curl/curl.h>
#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <stdlib.h>

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

    /* Use first byte to select a file path prefix */
    const char *path_prefix;
    switch (data[0] % 3) {
        case 0:
            path_prefix = "file:///tmp/fuzz_";
            break;
        case 1:
            path_prefix = "file://./fuzz_";
            break;
        default:
            path_prefix = "file://fuzz_";
            break;
    }

    /* Use second byte to select a suffix */
    const char *suffix;
    switch (data[1] % 4) {
        case 0:
            suffix = ".txt";
            break;
        case 1:
            suffix = ".dat";
            break;
        case 2:
            suffix = "";
            break;
        default:
            suffix = "/";
            break;
    }

    /* Build a bounded file URL from the remaining input bytes */
    size_t max_name_len = 64;
    size_t avail = size - 2;
    if (avail > max_name_len) {
        avail = max_name_len;
    }

    char *url = (char *)malloc(strlen(path_prefix) + avail + strlen(suffix) + 1);
    if (!url) {
        curl_easy_cleanup(curl);
        return 0;
    }

    strcpy(url, path_prefix);
    for (size_t i = 0; i < avail; i++) {
        char c = (char)data[2 + i];
        /* Keep the URL path printable and safe */
        if (c >= 0x20 && c <= 0x7e && c != '?' && c != '#' && c != '%') {
            url[strlen(path_prefix) + i] = c;
        } else {
            url[strlen(path_prefix) + i] = '_';
        }
    }
    url[strlen(path_prefix) + avail] = '\0';
    strcat(url, suffix);

    curl_easy_setopt(curl, CURLOPT_URL, url);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_cb);
    curl_easy_setopt(curl, CURLOPT_NOSIGNAL, 1L);
    curl_easy_setopt(curl, CURLOPT_CONNECTTIMEOUT_MS, 100L);
    curl_easy_setopt(curl, CURLOPT_TIMEOUT_MS, 100L);
    curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 0L);

    /* Use a bounded output buffer as an alternative sink */
    char outbuf[256];
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, outbuf);

    curl_easy_perform(curl);

    curl_easy_cleanup(curl);
    free(url);

    return 0;
}