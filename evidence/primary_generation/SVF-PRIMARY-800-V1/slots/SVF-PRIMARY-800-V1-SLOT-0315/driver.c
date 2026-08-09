#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include "cJSON.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) {
        return 0;
    }

    // Use first byte for options, second byte for a boolean flag
    int options = data[0] & 0x03; // Only use low 2 bits: 0, 1, 2, 3
    int require_null_terminated = data[1] & 0x01;

    // Remaining bytes are the JSON input
    const char *json = (const char *)(data + 2);
    size_t json_len = size - 2;

    // Ensure the input is not too large to avoid excessive memory usage
    if (json_len > 1024 * 1024) {
        return 0;
    }

    cJSON *item = cJSON_ParseWithLengthOpts(json, json_len, NULL, options);
    if (item != NULL) {
        cJSON_Delete(item);
    }

    return 0;
}