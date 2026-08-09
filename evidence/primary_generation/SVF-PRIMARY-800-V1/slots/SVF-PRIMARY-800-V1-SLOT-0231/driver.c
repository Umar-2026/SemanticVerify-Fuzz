#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <stdio.h>
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

    // Split input into two parts: first half for file1, second half for file2
    size_t half = size / 2;
    const uint8_t *data1 = data;
    size_t size1 = half;
    const uint8_t *data2 = data + half;
    size_t size2 = size - half;

    // Create temporary files
    char path1[] = "/tmp/curl_fuzz_XXXXXX";
    char path2[] = "/tmp/curl_fuzz_XXXXXX";
    int fd1 = mkstemp(path1);
    int fd2 = mkstemp(path2);
    if (fd1 < 0 || fd2 < 0) {
        if (fd1 >= 0) close(fd1);
        if (fd2 >= 0) close(fd2);
        return 0;
    }

    // Write data to files
    ssize_t written1 = write(fd1, data1, size1);
    ssize_t written2 = write(fd2, data2, size2);
    close(fd1);
    close(fd2);
    if (written1 != (ssize_t)size1 || written2 != (ssize_t)size2) {
        unlink(path1);
        unlink(path2);
        return 0;
    }

    // Build file URLs
    char url1[256];
    char url2[256];
    snprintf(url1, sizeof(url1), "file://%s", path1);
    snprintf(url2, sizeof(url2), "file://%s", path2);

    CURL *curl = curl_easy_init();
    if (!curl) {
        unlink(path1);
        unlink(path2);
        return 0;
    }

    // First transfer
    curl_easy_setopt(curl, CURLOPT_URL, url1);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, NULL);
    curl_easy_perform(curl);

    // Second transfer with same handle
    curl_easy_setopt(curl, CURLOPT_URL, url2);
    curl_easy_perform(curl);

    curl_easy_cleanup(curl);

    unlink(path1);
    unlink(path2);

    return 0;
}