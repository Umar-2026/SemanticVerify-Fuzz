#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include "cJSON.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) {
        return 0;
    }

    // Split the input into two parts at a delimiter byte (0xFF)
    size_t split_pos = 0;
    for (size_t i = 0; i < size; i++) {
        if (data[i] == 0xFF) {
            split_pos = i;
            break;
        }
    }

    if (split_pos == 0 || split_pos == size - 1) {
        return 0;
    }

    // First document
    const char *doc1 = (const char *)data;
    size_t len1 = split_pos;

    // Second document
    const char *doc2 = (const char *)(data + split_pos + 1);
    size_t len2 = size - split_pos - 1;

    // Parse first document
    cJSON *json1 = cJSON_ParseWithLength(doc1, len1);
    if (json1 != NULL) {
        // Process first document: just free it
        cJSON_Delete(json1);
    }

    // Parse second document
    cJSON *json2 = cJSON_ParseWithLength(doc2, len2);
    if (json2 != NULL) {
        // Process second document: just free it
        cJSON_Delete(json2);
    }

    return 0;
}