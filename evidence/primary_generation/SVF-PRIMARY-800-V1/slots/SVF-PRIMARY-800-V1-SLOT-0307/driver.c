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
    if (json != NULL) {
        // Inspect one value from the tree: the root item's type and value string
        if (cJSON_IsString(json) && json->valuestring != NULL) {
            // Access the string value to ensure it's valid
            volatile char c = json->valuestring[0];
            (void)c;
        } else if (cJSON_IsNumber(json)) {
            volatile double d = json->valuedouble;
            (void)d;
        } else if (cJSON_IsArray(json) || cJSON_IsObject(json)) {
            // Access the first child if present
            if (json->child != NULL) {
                volatile int type = json->child->type;
                (void)type;
            }
        }
        cJSON_Delete(json);
    }

    free(input);
    return 0;
}