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
        // Access item fields to ensure the iteration is exercised
        if (cJSON_IsString(item)) {
            // Just touch the value
            if (item->valuestring != NULL) {
                volatile size_t len = strlen(item->valuestring);
                (void)len;
            }
        } else if (cJSON_IsNumber(item)) {
            volatile double val = item->valuedouble;
            (void)val;
        } else if (cJSON_IsArray(item) || cJSON_IsObject(item)) {
            // Recursively iterate nested containers
            cJSON *nested = NULL;
            cJSON_ArrayForEach(nested, item) {
                // Touch nested items
                if (cJSON_IsString(nested)) {
                    if (nested->valuestring != NULL) {
                        volatile size_t len = strlen(nested->valuestring);
                        (void)len;
                    }
                } else if (cJSON_IsNumber(nested)) {
                    volatile double val = nested->valuedouble;
                    (void)val;
                }
            }
        }
    }

    cJSON_Delete(root);
    return 0;
}