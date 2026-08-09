#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include "cJSON.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) {
        return 0;
    }

    // Derive options from the first byte
    int options = data[0] & 0x03; // Use only bits 0 and 1 for options (0, 1, 2, 3)
    // Derive a length from the second byte, but ensure it does not exceed the remaining input size
    size_t length = data[1];
    if (length > size - 2) {
        length = size - 2;
    }

    // Use the remaining bytes as the JSON input
    const char *json = (const char *)(data + 2);
    size_t json_len = size - 2;

    // Allocate a buffer for the return pointer (to track how much was parsed)
    const char *end_ptr = NULL;

    // Parse with length and options
    cJSON *item = cJSON_ParseWithLengthOpts(json, json_len, &end_ptr, options);

    // If parsing succeeded, delete the item
    if (item != NULL) {
        cJSON_Delete(item);
    }

    return 0;
}