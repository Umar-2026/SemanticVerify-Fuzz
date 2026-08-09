#include <stdint.h>
#include <stddef.h>
#include "cJSON.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) {
        return 0;
    }

    uint8_t options_byte = data[0];
    size_t parse_size = size - 1;
    const char *json_data = (const char *)&data[1];

    cJSON_bool require_null_terminated = (options_byte & 0x01) != 0;
    cJSON_ParseOpts opts = {
        .require_null_terminated = require_null_terminated
    };

    const char *return_parse_end = NULL;

    cJSON *root = cJSON_ParseWithLengthOpts(json_data, parse_size, &return_parse_end, &opts);

    if (root != NULL) {
        cJSON_Delete(root);
    }

    return 0;
}