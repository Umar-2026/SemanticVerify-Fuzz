#include <stdint.h>
#include <stddef.h>
#include "cJSON.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) {
        return 0;
    }

    size_t split_point = data[0] % size;
    const char *json1 = (const char *)&data[1];
    size_t len1 = split_point;
    const char *json2 = (const char *)&data[split_point + 1];
    size_t len2 = size - split_point - 1;

    cJSON *root1 = cJSON_ParseWithLength(json1, len1);
    if (root1 != NULL) {
        cJSON_Delete(root1);
    }

    cJSON *root2 = cJSON_ParseWithLength(json2, len2);
    if (root2 != NULL) {
        cJSON_Delete(root2);
    }

    return 0;
}