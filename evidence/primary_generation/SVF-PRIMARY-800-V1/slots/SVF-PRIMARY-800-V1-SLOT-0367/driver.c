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
    // Use the first byte as a simple delimiter position hint, but ensure it's valid.
    size_t split = data[0] % (size - 1) + 1; // split in [1, size-1]

    const uint8_t *first_data = data;
    size_t first_size = split;
    const uint8_t *second_data = data + split;
    size_t second_size = size - split;

    // Parse the first JSON document
    cJSON *first = cJSON_ParseWithLength((const char *)first_data, first_size);
    if (first != NULL) {
        // Process first document: just delete it to keep it simple
        cJSON_Delete(first);
    }

    // Parse the second JSON document
    cJSON *second = cJSON_ParseWithLength((const char *)second_data, second_size);
    if (second != NULL) {
        // Process second document: just delete it
        cJSON_Delete(second);
    }

    return 0;
}