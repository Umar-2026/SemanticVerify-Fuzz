#include <stddef.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>

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

    // Split input into two parts
    size_t split = size / 2;
    const uint8_t *part1 = data;
    size_t part1_size = split;
    const uint8_t *part2 = data + split;
    size_t part2_size = size - split;

    // Create temporary files
    char template1[] = "/tmp/curl_fuzz_XXXXXX";
    char template2[] = "/tmp/curl_fuzz_XXXXXX";
    int fd1 = mkstemp(template1);
    int fd2 = mkstemp(template2);
    if (fd1 < 0 || fd2 < 0) {
        if (fd1 >= 0) close(fd1);
        if (fd2 >= 0) close(fd2);
        return 0;
    }

    // Write data to files
    ssize_t written1 = write(fd1, part1, part1_size);
    ssize_t written2 = write(fd2, part2, part2_size);
    close(fd1);
    close(fd2);
    if (written1 != (ssize_t)part1_size || written2 != (ssize_t)part2_size) {
        unlink(template1);
        unlink(template2);
        return 0;
    }

    // Build file URLs
    char url1[512];
    char url2[512];
    snprintf(url1, sizeof(url1), "file://%s", template1);
    snprintf(url2, sizeof(url2), "file://%s", template2);

    CURL *curl = curl_easy_init();
    if (!curl) {
        unlink(template1);
        unlink(template2);
        return 0;
    }

    // First transfer
    curl_easy_setopt(curl, CURLOPT_URL, url1);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
    curl_easy_setopt(curl, CURLOPT_NOSIGNAL, 1L);
    curl_easy_perform(curl);

    // Second transfer with same handle
    curl_easy_setopt(curl, CURLOPT_URL, url2);
    curl_easy_perform(curl);

    curl_easy_cleanup(curl);

    unlink(template1);
    unlink(template2);

    return 0;
}