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
        // Inspect one value from the tree: the root item's type and value
        // This exercises the parsed tree without requiring additional symbols.
        if (cJSON_IsObject(json)) {
            // Access a child if present
            cJSON *child = json->child;
            if (child != NULL) {
                // Just touch the child to ensure it's valid
                volatile int type = child->type;
                (void)type;
            }
        } else if (cJSON_IsArray(json)) {
            cJSON *child = json->child;
            if (child != NULL) {
                volatile int type = child->type;
                (void)type;
            }
        } else {
            // For primitive types, just check the type
            volatile int type = json->type;
            (void)type;
        }

        cJSON_Delete(json);
    }

    free(input);
    return 0;
}