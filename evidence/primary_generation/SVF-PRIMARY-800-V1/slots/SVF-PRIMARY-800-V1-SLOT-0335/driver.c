#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include "cJSON.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size == 0) {
        return 0;
    }

    // Ensure input is null-terminated for cJSON_Parse
    char *json_str = (char *)malloc(size + 1);
    if (!json_str) {
        return 0;
    }
    memcpy(json_str, data, size);
    json_str[size] = '\0';

    cJSON *root = cJSON_Parse(json_str);
    free(json_str);

    if (root == NULL) {
        return 0;
    }

    // Iterate over all items in the root if it's an array or object
    cJSON *item = NULL;
    cJSON_ArrayForEach(item, root) {
        // Access item fields to ensure the iteration is exercised
        if (item->type == cJSON_String) {
            // Just touch the value
            if (item->valuestring != NULL) {
                volatile char c = item->valuestring[0];
                (void)c;
            }
        } else if (item->type == cJSON_Number) {
            volatile double d = item->valuedouble;
            (void)d;
        } else if (item->type == cJSON_Array || item->type == cJSON_Object) {
            // Recursively iterate nested structures
            cJSON *nested = NULL;
            cJSON_ArrayForEach(nested, item) {
                // Touch nested item
                if (nested->type == cJSON_String && nested->valuestring != NULL) {
                    volatile char c = nested->valuestring[0];
                    (void)c;
                }
            }
        }
    }

    cJSON_Delete(root);
    return 0;
}