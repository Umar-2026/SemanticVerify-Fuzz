#include <stdint.h>
#include <stddef.h>
#include "cJSON.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size == 0) {
        return 0;
    }

    char *json_str = (char *)malloc(size + 1);
    if (!json_str) {
        return 0;
    }
    memcpy(json_str, data, size);
    json_str[size] = '\0';

    cJSON *root = cJSON_Parse(json_str);
    if (root != NULL) {
        cJSON *item = cJSON_GetObjectItem(root, "test_key");
        if (item != NULL) {
            if (cJSON_IsString(item)) {
                const char *val = item->valuestring;
                (void)val;
            }
        }
        cJSON_Delete(root);
    }

    free(json_str);
    return 0;
}