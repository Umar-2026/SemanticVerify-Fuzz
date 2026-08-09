#include <stdio.h>
#include <stdlib.h>
#include <string.h>
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
    const uint8_t *data1 = data;
    size_t size1 = split;
    const uint8_t *data2 = data + split;
    size_t size2 = size - split;

    // Create temporary file names
    char file1[] = "/tmp/curl_fuzz_XXXXXX";
    char file2[] = "/tmp/curl_fuzz_XXXXXX";
    int fd1 = mkstemp(file1);
    int fd2 = mkstemp(file2);
    if (fd1 == -1 || fd2 == -1) {
        if (fd1 != -1) close(fd1);
        if (fd2 != -1) close(fd2);
        return 0;
    }

    // Write data to files
    ssize_t written1 = write(fd1, data1, size1);
    ssize_t written2 = write(fd2, data2, size2);
    close(fd1);
    close(fd2);
    if (written1 != (ssize_t)size1 || written2 != (ssize_t)size2) {
        unlink(file1);
        unlink(file2);
        return 0;
    }

    // Construct file URLs
    char url1[512];
    char url2[512];
    snprintf(url1, sizeof(url1), "file://%s", file1);
    snprintf(url2, sizeof(url2), "file://%s", file2);

    CURL *easy1 = curl_easy_init();
    CURL *easy2 = curl_easy_init();
    if (!easy1 || !easy2) {
        if (easy1) curl_easy_cleanup(easy1);
        if (easy2) curl_easy_cleanup(easy2);
        unlink(file1);
        unlink(file2);
        return 0;
    }

    // Configure and perform first transfer
    curl_easy_setopt(easy1, CURLOPT_URL, url1);
    curl_easy_setopt(easy1, CURLOPT_WRITEFUNCTION, write_callback);
    curl_easy_setopt(easy1, CURLOPT_NOSIGNAL, 1L);
    CURLcode res1 = curl_easy_perform(easy1);

    // Configure and perform second transfer
    curl_easy_setopt(easy2, CURLOPT_URL, url2);
    curl_easy_setopt(easy2, CURLOPT_WRITEFUNCTION, write_callback);
    curl_easy_setopt(easy2, CURLOPT_NOSIGNAL, 1L);
    CURLcode res2 = curl_easy_perform(easy2);

    // Cleanup
    curl_easy_cleanup(easy1);
    curl_easy_cleanup(easy2);
    unlink(file1);
    unlink(file2);

    (void)res1;
    (void)res2;
    return 0;
}