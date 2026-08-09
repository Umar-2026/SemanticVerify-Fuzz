#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>

#include <curl/curl.h>

#define MAX_FILE_SIZE 4096
#define MAX_FILENAME_LEN 64

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

    // Limit file sizes
    if (size1 > MAX_FILE_SIZE) size1 = MAX_FILE_SIZE;
    if (size2 > MAX_FILE_SIZE) size2 = MAX_FILE_SIZE;

    // Create temporary files
    char filename1[MAX_FILENAME_LEN];
    char filename2[MAX_FILENAME_LEN];
    snprintf(filename1, sizeof(filename1), "/tmp/curl_fuzz_%d_1", getpid());
    snprintf(filename2, sizeof(filename2), "/tmp/curl_fuzz_%d_2", getpid());

    int fd1 = open(filename1, O_WRONLY | O_CREAT | O_TRUNC, 0600);
    int fd2 = open(filename2, O_WRONLY | O_CREAT | O_TRUNC, 0600);
    if (fd1 < 0 || fd2 < 0) {
        if (fd1 >= 0) close(fd1);
        if (fd2 >= 0) close(fd2);
        return 0;
    }

    ssize_t written1 = write(fd1, data1, size1);
    ssize_t written2 = write(fd2, data2, size2);
    close(fd1);
    close(fd2);
    if (written1 != (ssize_t)size1 || written2 != (ssize_t)size2) {
        unlink(filename1);
        unlink(filename2);
        return 0;
    }

    // Build file:// URLs
    char url1[256];
    char url2[256];
    snprintf(url1, sizeof(url1), "file://%s", filename1);
    snprintf(url2, sizeof(url2), "file://%s", filename2);

    CURL *curl = curl_easy_init();
    if (!curl) {
        unlink(filename1);
        unlink(filename2);
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

    unlink(filename1);
    unlink(filename2);

    return 0;
}