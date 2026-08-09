#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <curl/curl.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size == 0 || size > 1024 * 1024) {
        return 0;
    }

    char filename[] = "/tmp/fuzz_curl_XXXXXX";
    int fd = mkstemp(filename);
    if (fd < 0) {
        return 0;
    }

    if (write(fd, data, size) != (ssize_t)size) {
        close(fd);
        unlink(filename);
        return 0;
    }
    close(fd);

    CURL *curl = curl_easy_init();
    if (curl) {
        char url[1024];
        snprintf(url, sizeof(url), "file://%s", filename);

        curl_easy_setopt(curl, CURLOPT_URL, url);
        curl_easy_setopt(curl, CURLOPT_TIMEOUT, 1L);
        curl_easy_setopt(curl, CURLOPT_NOPROGRESS, 1L);
        
        curl_easy_perform(curl);
        curl_easy_cleanup(curl);
    }

    unlink(filename);
    return 0;
}