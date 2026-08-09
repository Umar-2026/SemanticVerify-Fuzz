#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include "cJSON.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) {
        return 0;
    }

    // Use first byte to derive options
    int options = data[0] & 0x03; // Only use low 2 bits for options (0, 1, 2, 3)
    // Use second byte to derive require_null_terminated flag
    int require_null_terminated = data[1] & 0x01;

    // Remaining data is the JSON string
    const char *json = (const char *)(data + 2);
    size_t json_len = size - 2;

    // Ensure the buffer is null-terminated for safety, but we use length-based parsing
    char *buffer = (char *)malloc(json_len + 1);
    if (!buffer) {
        return 0;
    }
    memcpy(buffer, json, json_len);
    buffer[json_len] = '\0';

    const char *end_ptr = NULL;
    cJSON *item = cJSON_ParseWithLengthOpts(buffer, json_len, &end_ptr, options, require_null_terminated);

    if (item != NULL) {
        cJSON_Delete(item);
    }

    free(buffer);
    return 0;
}