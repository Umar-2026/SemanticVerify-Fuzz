#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>

struct MemoryBuffer {
    char *data;
    size_t size;
};

static size_t write_callback(void *contents, size_t size, size_t nmemb, void *userp) {
    size_t realsize = size * nmemb;
    struct MemoryBuffer *mem = (struct MemoryBuffer *)userp;

    char *ptr = realloc(mem->data, mem->size + realsize + 1);
    if (!ptr) {
        fprintf(stderr, "Not enough memory\n");
        return 0;
    }

    mem->data = ptr;
    memcpy(&(mem->data[mem->size]), contents, realsize);
    mem->size += realsize;
    mem->data[mem->size] = 0;

    return realsize;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    CURL *curl;
    CURLcode res;
    struct MemoryBuffer chunk = {0};

    if (size < 1) {
        return 0;
    }

    // Construct a file:// URL from the fuzz input. Use a temporary file.
    char tmpfile[] = "/tmp/curl_fuzz_XXXXXX";
    int fd = mkstemp(tmpfile);
    if (fd == -1) {
        return 0;
    }

    // Write fuzz data to the temporary file
    ssize_t written = write(fd, data, size);
    if (written != (ssize_t)size) {
        close(fd);
        unlink(tmpfile);
        return 0;
    }
    close(fd);

    // Build the file:// URL
    char url[512];
    snprintf(url, sizeof(url), "file://%s", tmpfile);

    curl_global_init(CURL_GLOBAL_DEFAULT);
    curl = curl_easy_init();
    if (!curl) {
        unlink(tmpfile);
        curl_global_cleanup();
        return 0;
    }

    curl_easy_setopt(curl, CURLOPT_URL, url);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, (void *)&chunk);
    curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 0L);
    curl_easy_setopt(curl, CURLOPT_MAXREDIRS, 0L);
    curl_easy_setopt(curl, CURLOPT_TIMEOUT, 5L);
    curl_easy_setopt(curl, CURLOPT_CONNECTTIMEOUT, 5L);

    res = curl_easy_perform(curl);

    // Cleanup
    curl_easy_cleanup(curl);
    curl_global_cleanup();

    if (chunk.data) {
        free(chunk.data);
    }

    unlink(tmpfile);

    return 0;
}