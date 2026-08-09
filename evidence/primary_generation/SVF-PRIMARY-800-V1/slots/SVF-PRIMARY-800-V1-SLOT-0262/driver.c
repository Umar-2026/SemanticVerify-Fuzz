#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>
#include <unistd.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 10) return 0;

    size_t split = size / 2;
    char path1[] = "/tmp/fuzz1.txt";
    char path2[] = "/tmp/fuzz2.txt";

    FILE *f1 = fopen(path1, "wb");
    if (!f1) return 0;
    fwrite(data, 1, split, f1);
    fclose(f1);

    FILE *f2 = fopen(path2, "wb");
    if (!f2) return 0;
    fwrite(data + split, 1, size - split, f2);
    fclose(f2);

    CURL *curl1 = curl_easy_init();
    CURL *curl2 = curl_easy_init();

    if (curl1 && curl2) {
        char url1[64];
        char url2[64];
        snprintf(url1, sizeof(url1), "file://%s", path1);
        snprintf(url2, sizeof(url2), "file://%s", path2);

        curl_easy_setopt(curl1, CURLOPT_URL, url1);
        curl_easy_setopt(curl1, CURLOPT_TIMEOUT, 1L);
        curl_easy_setopt(curl1, CURLOPT_NOPROGRESS, 1L);

        curl_easy_setopt(curl2, CURLOPT_URL, url2);
        curl_easy_setopt(curl2, CURLOPT_TIMEOUT, 1L);
        curl_easy_setopt(curl2, CURLOPT_NOPROGRESS, 1L);

        curl_easy_perform(curl1);
        curl_easy_perform(curl2);
    }

    if (curl1) curl_easy_cleanup(curl1);
    if (curl2) curl_easy_cleanup(curl2);

    unlink(path1);
    unlink(path2);

    return 0;
}