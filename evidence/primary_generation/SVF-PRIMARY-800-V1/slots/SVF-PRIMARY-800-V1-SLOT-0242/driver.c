#include <stdio.h>
#include <stdlib.h>
#include <curl/curl.h>

int main(int argc, char **argv) {
    if (argc < 3) return 0;

    CURL *curl;
    CURLcode res;

    curl_global_init(CURL_GLOBAL_ALL);
    curl = curl_easy_init();

    if (curl) {
        /* First operation */
        curl_easy_setopt(curl, CURLOPT_URL, argv[1]);
        curl_easy_setopt(curl, CURLOPT_FILETIME, 1L);
        res = curl_easy_perform(curl);

        /* Reset handle */
        curl_easy_reset(curl);

        /* Second operation */
        curl_easy_setopt(curl, CURLOPT_URL, argv[2]);
        curl_easy_setopt(curl, CURLOPT_VERBOSE, 1L);
        res = curl_easy_perform(curl);

        curl_easy_cleanup(curl);
    }

    curl_global_cleanup();
    return 0;
}