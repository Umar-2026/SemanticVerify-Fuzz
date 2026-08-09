#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include "cJSON.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) {
        return 0;
    }

    // Find a delimiter to split the input into two parts.
    // Use the first byte as a simple delimiter value (0-255).
    uint8_t delimiter = data[0];
    size_t split_pos = 0;
    for (size_t i = 1; i < size; i++) {
        if (data[i] == delimiter) {
            split_pos = i;
            break;
        }
    }

    if (split_pos == 0) {
        // No delimiter found, treat entire input as one document.
        cJSON *json1 = cJSON_ParseWithLength((const char *)data, size);
        if (json1 != NULL) {
            cJSON_Delete(json1);
        }
        return 0;
    }

    // First document: bytes [1, split_pos)
    size_t len1 = split_pos - 1;
    const char *doc1 = (const char *)data + 1;

    // Second document: bytes [split_pos+1, size)
    size_t len2 = size - split_pos - 1;
    const char *doc2 = (const char *)data + split_pos + 1;

    // Parse first document
    cJSON *json1 = cJSON_ParseWithLength(doc1, len1);
    if (json1 != NULL) {
        // Process first document (e.g., validate or extract)
        cJSON_Delete(json1);
    }

    // Parse second document
    cJSON *json2 = cJSON_ParseWithLength(doc2, len2);
    if (json2 != NULL) {
        // Process second document
        cJSON_Delete(json2);
    }

    return 0;
}