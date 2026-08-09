#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>

static size_t write_callback(void *contents, size_t size, size_t nmemb, void *userp) {
    return size * nmemb;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 10) return 0;

    char *filename = malloc(size + 1);
    if (!filename) return 0;
    memcpy(filename, data, size);
    filename[size] = '\0';

    CURL *curl = curl_easy_init();
    if (curl) {
        char url[2048];
        snprintf(url, sizeof(url), "file://%s", filename);

        curl_easy_setopt(curl, CURLOPT_URL, url);
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
        curl_easy_setopt(curl, CURLOPT_TIMEOUT, 1L);
        curl_easy_setopt(curl, CURLOPT_NOPROGRESS, 1L);

        curl_easy_perform(curl);
        curl_easy_cleanup(curl);
    }

    free(filename);
    return 0;
}

int main(int argc, char **argv) {
    curl_global_init(CURL_GLOBAL_ALL);
    if (argc > 1) {
        FILE *f = fopen(argv[1], "rb");
        if (f) {
            fseek(f, 0, SEEK_END);
            long fsize = ftell(f);
            fseek(f, 0, SEEK_SET);
            uint8_t *buf = malloc(fsize);
            fread(buf, 1, fsize, f);
            LLVMFuzzerTestOneInput(buf, fsize);
            free(buf);
            fclose(f);
        }
    }
    curl_global_cleanup();
    return 0;
}