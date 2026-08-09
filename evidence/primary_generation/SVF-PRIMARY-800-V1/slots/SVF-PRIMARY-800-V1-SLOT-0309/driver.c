#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include "cJSON.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size == 0) {
        return 0;
    }

    // Ensure the input is null-terminated for cJSON_Parse
    char *input = (char *)malloc(size + 1);
    if (input == NULL) {
        return 0;
    }
    memcpy(input, data, size);
    input[size] = '\0';

    cJSON *json = cJSON_Parse(input);
    free(input);

    if (json != NULL) {
        // Inspect one value from the resulting tree
        // For example, check if the root is an object and get the first item
        if (cJSON_IsObject(json)) {
            cJSON *first_item = json->child;
            if (first_item != NULL) {
                // Access the value type and string representation
                if (cJSON_IsString(first_item) && first_item->valuestring != NULL) {
                    // Just touch the string to ensure it's valid
                    volatile size_t len = strlen(first_item->valuestring);
                    (void)len;
                } else if (cJSON_IsNumber(first_item)) {
                    volatile double val = first_item->valuedouble;
                    (void)val;
                }
            }
        } else if (cJSON_IsArray(json)) {
            cJSON *first_item = json->child;
            if (first_item != NULL) {
                if (cJSON_IsString(first_item) && first_item->valuestring != NULL) {
                    volatile size_t len = strlen(first_item->valuestring);
                    (void)len;
                } else if (cJSON_IsNumber(first_item)) {
                    volatile double val = first_item->valuedouble;
                    (void)val;
                }
            }
        }

        cJSON_Delete(json);
    }

    return 0;
}