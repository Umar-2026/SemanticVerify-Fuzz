#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <curl/curl.h>

static size_t write_callback(char *ptr, size_t size, size_t nmemb, void *userdata) {
    (void)ptr;
    (void)userdata;
    return size * nmemb;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) {
        return 0;
    }

    // Limit the file content size to avoid excessive memory usage
    size_t content_size = size - 1;
    if (content_size > 4096) {
        content_size = 4096;
    }

    // Create a temporary file with fuzz-derived content
    char template[] = "/tmp/curl_fuzz_XXXXXX";
    int fd = mkstemp(template);
    if (fd == -1) {
        return 0;
    }

    ssize_t written = write(fd, data, content_size);
    if (written != (ssize_t)content_size) {
        close(fd);
        unlink(template);
        return 0;
    }
    close(fd);

    // Construct file:// URL
    char url[512];
    snprintf(url, sizeof(url), "file://%s", template);

    CURL *curl = curl_easy_init();
    if (!curl) {
        unlink(template);
        return 0;
    }

    curl_easy_setopt(curl, CURLOPT_URL, url);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
    curl_easy_setopt(curl, CURLOPT_NOSIGNAL, 1L);
    curl_easy_setopt(curl, CURLOPT_CONNECTTIMEOUT_MS, 1000L);
    curl_easy_setopt(curl, CURLOPT_TIMEOUT_MS, 1000L);

    CURLcode res = curl_easy_perform(curl);

    curl_easy_cleanup(curl);
    unlink(template);

    return 0;
}