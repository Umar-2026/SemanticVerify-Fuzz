#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include "cJSON.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) {
        return 0;
    }

    // Split the input into two parts at a random point determined by the first byte.
    size_t split = data[0] % (size - 1) + 1;
    const uint8_t *first_data = data + 1;
    size_t first_size = split - 1;
    const uint8_t *second_data = data + split;
    size_t second_size = size - split;

    // Parse the first JSON document.
    cJSON *first = cJSON_ParseWithLength((const char *)first_data, first_size);
    if (first != NULL) {
        // Process the first document: just free it.
        cJSON_Delete(first);
    }

    // Parse the second JSON document.
    cJSON *second = cJSON_ParseWithLength((const char *)second_data, second_size);
    if (second != NULL) {
        // Process the second document: just free it.
        cJSON_Delete(second);
    }

    return 0;
}