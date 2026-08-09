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
    int options = data[0] & 0x01; // cJSON_RejectNull or 0
    size_t length = data[1];
    if (length > size - 2) {
        length = size - 2;
    }

    const char *json = (const char *)(data + 2);
    const char *end_ptr = NULL;

    cJSON *item = cJSON_ParseWithLengthOpts(json, length, &end_ptr, options);
    if (item != NULL) {
        cJSON_Delete(item);
    }

    return 0;
}