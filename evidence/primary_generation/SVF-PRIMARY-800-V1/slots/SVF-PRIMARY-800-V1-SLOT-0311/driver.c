#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include "cJSON.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) {
        return 0;
    }

    // Use first byte for options, second byte for length hint
    int options = data[0] & 0x03; // cJSON_RejectNull or cJSON_AllowNull
    size_t length = size - 2;
    if (length > 0 && data[1] != 0) {
        // Use second byte to potentially limit length, but keep it within bounds
        size_t hint = data[1];
        if (hint < length) {
            length = hint;
        }
    }

    const char *json = (const char *)data + 2;
    const char *end_ptr = NULL;

    cJSON *item = cJSON_ParseWithLengthOpts(json, length, &end_ptr, options);
    if (item != NULL) {
        cJSON_Delete(item);
    }

    return 0;
}