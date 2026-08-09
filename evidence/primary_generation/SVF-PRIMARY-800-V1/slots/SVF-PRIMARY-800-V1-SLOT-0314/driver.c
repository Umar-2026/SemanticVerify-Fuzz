#include <stdint.h>
#include <stddef.h>
#include "cJSON.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) {
        return 0;
    }

    uint8_t options_byte = data[0];
    const char *json_data = (const char *)&data[1];
    size_t json_size = size - 1;

    cJSON_bool require_null_terminated = (options_byte & 0x01) != 0;
    cJSON_bool *return_parse_end = NULL;

    cJSON *root = cJSON_ParseWithLengthOpts(
        json_data,
        json_size,
        (const char **)&return_parse_end,
        require_null_terminated
    );

    if (root != NULL) {
        cJSON_Delete(root);
    }

    return 0;
}