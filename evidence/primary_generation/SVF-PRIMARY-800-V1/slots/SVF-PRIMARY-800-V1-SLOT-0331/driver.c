#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include "cJSON.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size == 0) {
        return 0;
    }

    // Ensure input is null-terminated for cJSON_Parse
    char *input = (char *)malloc(size + 1);
    if (!input) {
        return 0;
    }
    memcpy(input, data, size);
    input[size] = '\0';

    cJSON *root = cJSON_Parse(input);
    free(input);

    if (root == NULL) {
        return 0;
    }

    // Iterate over all items in the root if it's an array or object
    cJSON *item = NULL;
    cJSON_ArrayForEach(item, root) {
        // Access item fields to exercise the iteration
        if (cJSON_IsString(item)) {
            // Just touch the value
            volatile const char *s = item->valuestring;
            (void)s;
        } else if (cJSON_IsNumber(item)) {
            volatile double d = item->valuedouble;
            (void)d;
        } else if (cJSON_IsObject(item) || cJSON_IsArray(item)) {
            // Recursively iterate nested containers (bounded by input size)
            cJSON *nested = NULL;
            cJSON_ArrayForEach(nested, item) {
                // Touch nested item
                if (cJSON_IsString(nested)) {
                    volatile const char *s = nested->valuestring;
                    (void)s;
                }
            }
        }
    }

    cJSON_Delete(root);
    return 0;
}