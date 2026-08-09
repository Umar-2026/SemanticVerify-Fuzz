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

    cJSON *root = cJSON_Parse(input);
    if (root != NULL) {
        // Inspect one value from the tree: check if it's an object and get a key
        if (cJSON_IsObject(root)) {
            cJSON *first_item = root->child;
            if (first_item != NULL) {
                // Access the value string or number to ensure the tree is traversed
                if (cJSON_IsString(first_item) && first_item->valuestring != NULL) {
                    // Just touch the string to prevent optimization
                    volatile char c = first_item->valuestring[0];
                    (void)c;
                } else if (cJSON_IsNumber(first_item)) {
                    volatile double d = first_item->valuedouble;
                    (void)d;
                }
            }
        }
        cJSON_Delete(root);
    }

    free(input);
    return 0;
}