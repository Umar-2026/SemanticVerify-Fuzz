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
        // Inspect one value from the resulting tree
        cJSON *item = json->child;
        if (item != NULL) {
            // Access the value to ensure it's valid
            volatile int dummy = 0;
            if (cJSON_IsString(item)) {
                dummy = (int)strlen(item->valuestring);
            } else if (cJSON_IsNumber(item)) {
                dummy = (int)item->valuedouble;
            } else if (cJSON_IsBool(item)) {
                dummy = item->valueint;
            }
            (void)dummy;
        }
        cJSON_Delete(json);
    }

    free(input);
    return 0;
}