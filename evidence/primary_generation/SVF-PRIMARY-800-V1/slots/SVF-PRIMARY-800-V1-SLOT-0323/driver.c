#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include "cJSON.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size == 0) {
        return 0;
    }

    // Use a bounded portion of the input as the JSON string.
    // Limit the length to avoid excessive memory usage.
    size_t json_len = size;
    if (json_len > 1024 * 1024) {
        json_len = 1024 * 1024;
    }

    // cJSON_ParseWithLength expects a null-terminated string, but we can pass
    // a buffer that is not null-terminated as long as we provide the length.
    // However, to be safe, we copy the data into a buffer with a null terminator.
    char *json_str = (char *)malloc(json_len + 1);
    if (!json_str) {
        return 0;
    }
    memcpy(json_str, data, json_len);
    json_str[json_len] = '\0';

    cJSON *root = cJSON_ParseWithLength(json_str, json_len);
    if (root == NULL) {
        free(json_str);
        return 0;
    }

    // Process selected values from the parsed tree.
    // We'll look for a "value" key if it's an object, or if it's an array,
    // we'll process the first element if it's a number.
    cJSON *item = NULL;
    if (cJSON_IsObject(root)) {
        item = cJSON_GetObjectItemCaseSensitive(root, "value");
    } else if (cJSON_IsArray(root) && cJSON_GetArraySize(root) > 0) {
        item = cJSON_GetArrayItem(root, 0);
    }

    if (item != NULL) {
        if (cJSON_IsNumber(item)) {
            // Use the numeric value in a simple computation.
            double val = item->valuedouble;
            if (val > 0.0) {
                volatile double result = val * 2.0;
                (void)result;
            }
        } else if (cJSON_IsString(item)) {
            // Use the string value.
            const char *str = item->valuestring;
            if (str != NULL) {
                size_t len = strlen(str);
                if (len > 0) {
                    // Simple processing: check first character.
                    if (str[0] == 'a') {
                        // Do nothing, just exercise the path.
                    }
                }
            }
        } else if (cJSON_IsBool(item)) {
            // Use the boolean value.
            int b = cJSON_IsTrue(item);
            (void)b;
        }
    }

    cJSON_Delete(root);
    free(json_str);
    return 0;
}