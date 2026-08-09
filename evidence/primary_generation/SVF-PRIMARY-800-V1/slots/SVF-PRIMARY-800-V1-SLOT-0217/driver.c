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

    // Use first byte to select a local file path variant
    const char *path = "/tmp/fuzz_input";
    if (data[0] & 1) {
        path = "/etc/hostname";
    }

    // Build file:// URL
    char url[256];
    snprintf(url, sizeof(url), "file://%s", path);

    curl_easy_setopt(curl, CURLOPT_URL, url);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, NULL);

    // Bounded input-derived options
    if (size > 1) {
        long timeout = (long)(data[1] % 10);
        curl_easy_setopt(curl, CURLOPT_TIMEOUT, timeout);
    }
    if (size > 2) {
        long connect_timeout = (long)(data[2] % 5);
        curl_easy_setopt(curl, CURLOPT_CONNECTTIMEOUT, connect_timeout);
    }
    if (size > 3) {
        long low_speed_limit = (long)(data[3] % 100);
        curl_easy_setopt(curl, CURLOPT_LOW_SPEED_LIMIT, low_speed_limit);
    }
    if (size > 4) {
        long low_speed_time = (long)(data[4] % 30);
        curl_easy_setopt(curl, CURLOPT_LOW_SPEED_TIME, low_speed_time);
    }

    curl_easy_perform(curl);
    curl_easy_cleanup(curl);

    return 0;
}