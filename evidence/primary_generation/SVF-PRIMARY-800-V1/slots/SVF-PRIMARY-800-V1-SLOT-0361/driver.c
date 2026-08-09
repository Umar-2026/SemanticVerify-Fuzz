#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include "cJSON.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) {
        return 0;
    }

    // Find a delimiter to split the input into two parts.
    // Use the first byte as a hint for the split point, but ensure it's valid.
    size_t split = data[0];
    if (split >= size - 1) {
        split = size / 2;
    }

    // Ensure split is at least 1 and leaves at least 1 byte for the second document.
    if (split == 0) {
        split = 1;
    }
    if (split >= size) {
        split = size - 1;
    }

    // Parse the first document.
    cJSON *doc1 = cJSON_ParseWithLength((const char *)data + 1, split);
    if (doc1 != NULL) {
        cJSON_Delete(doc1);
    }

    // Parse the second document.
    size_t second_len = size - split - 1;
    if (second_len > 0) {
        cJSON *doc2 = cJSON_ParseWithLength((const char *)data + split + 1, second_len);
        if (doc2 != NULL) {
            cJSON_Delete(doc2);
        }
    }

    return 0;
}