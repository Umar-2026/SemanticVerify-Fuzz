#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>

static size_t discard_write(void *ptr, size_t size, size_t nmemb, void *userdata) {
    (void)ptr;
    (void)userdata;
    return size * nmemb;
}

static int write_file_data(const char *path, const unsigned char *data, size_t len) {
    FILE *f = fopen(path, "wb");
    if (!f) return -1;
    size_t written = fwrite(data, 1, len, f);
    fclose(f);
    return (written == len) ? 0 : -1;
}

int LLVMFuzzerTestOneInput(const unsigned char *data, size_t size) {
    if (size < 2) return 0;

    // Split input into two parts for two files
    size_t half = size / 2;
    const unsigned char *data1 = data;
    size_t size1 = half;
    const unsigned char *data2 = data + half;
    size_t size2 = size - half;

    // Create temporary file names
    char path1[] = "/tmp/curl_fuzz_s07_XXXXXX";
    char path2[] = "/tmp/curl_fuzz_s07_XXXXXX";
    int fd1 = mkstemp(path1);
    int fd2 = mkstemp(path2);
    if (fd1 == -1 || fd2 == -1) {
        if (fd1 != -1) close(fd1);
        if (fd2 != -1) close(fd2);
        return 0;
    }
    close(fd1);
    close(fd2);

    // Write data to files
    if (write_file_data(path1, data1, size1) != 0 ||
        write_file_data(path2, data2, size2) != 0) {
        unlink(path1);
        unlink(path2);
        return 0;
    }

    // Build file:// URLs
    char url1[4096];
    char url2[4096];
    snprintf(url1, sizeof(url1), "file://%s", path1);
    snprintf(url2, sizeof(url2), "file://%s", path2);

    CURL *curl1 = curl_easy_init();
    CURL *curl2 = curl_easy_init();
    if (!curl1 || !curl2) {
        if (curl1) curl_easy_cleanup(curl1);
        if (curl2) curl_easy_cleanup(curl2);
        unlink(path1);
        unlink(path2);
        return 0;
    }

    // Configure first handle
    curl_easy_setopt(curl1, CURLOPT_URL, url1);
    curl_easy_setopt(curl1, CURLOPT_WRITEFUNCTION, discard_write);
    curl_easy_setopt(curl1, CURLOPT_NOSIGNAL, 1L);
    curl_easy_setopt(curl1, CURLOPT_TIMEOUT_MS, 1000L);

    // Configure second handle
    curl_easy_setopt(curl2, CURLOPT_URL, url2);
    curl_easy_setopt(curl2, CURLOPT_WRITEFUNCTION, discard_write);
    curl_easy_setopt(curl2, CURLOPT_NOSIGNAL, 1L);
    curl_easy_setopt(curl2, CURLOPT_TIMEOUT_MS, 1000L);

    // Perform transfers independently
    CURLcode res1 = curl_easy_perform(curl1);
    CURLcode res2 = curl_easy_perform(curl2);

    // Cleanup
    curl_easy_cleanup(curl1);
    curl_easy_cleanup(curl2);
    unlink(path1);
    unlink(path2);

    (void)res1;
    (void)res2;
    return 0;
}