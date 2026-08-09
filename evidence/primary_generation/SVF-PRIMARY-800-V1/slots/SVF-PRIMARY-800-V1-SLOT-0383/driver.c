#include <stdlib.h>
#include <string.h>
#include <stdint.h>
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

    cJSON *json = cJSON_Parse(input);
    free(input);

    if (json == NULL) {
        return 0;
    }

    // Check for presence of "type" field and branch on its value
    cJSON *type_item = cJSON_GetObjectItemCaseSensitive(json, "type");
    if (type_item != NULL && cJSON_IsString(type_item)) {
        const char *type_str = type_item->valuestring;
        if (type_str != NULL) {
            if (strcmp(type_str, "number") == 0) {
                // Check for "value" field as number
                cJSON *value_item = cJSON_GetObjectItemCaseSensitive(json, "value");
                if (value_item != NULL && cJSON_IsNumber(value_item)) {
                    // Simulate numeric processing
                    double val = value_item->valuedouble;
                    if (val > 0) {
                        // Positive branch
                    } else {
                        // Non-positive branch
                    }
                }
            } else if (strcmp(type_str, "string") == 0) {
                // Check for "value" field as string
                cJSON *value_item = cJSON_GetObjectItemCaseSensitive(json, "value");
                if (value_item != NULL && cJSON_IsString(value_item)) {
                    // Simulate string processing
                    const char *str_val = value_item->valuestring;
                    if (str_val != NULL && str_val[0] != '\0') {
                        // Non-empty string branch
                    }
                }
            } else if (strcmp(type_str, "array") == 0) {
                // Check for "items" field as array
                cJSON *items_item = cJSON_GetObjectItemCaseSensitive(json, "items");
                if (items_item != NULL && cJSON_IsArray(items_item)) {
                    // Simulate array processing
                    int count = cJSON_GetArraySize(items_item);
                    if (count > 0) {
                        // Non-empty array branch
                    }
                }
            } else {
                // Unknown type branch
            }
        }
    }

    // Check for presence of "enabled" field as boolean
    cJSON *enabled_item = cJSON_GetObjectItemCaseSensitive(json, "enabled");
    if (enabled_item != NULL && cJSON_IsBool(enabled_item)) {
        if (cJSON_IsTrue(enabled_item)) {
            // Enabled true branch
        } else {
            // Enabled false branch
        }
    }

    cJSON_Delete(json);
    return 0;
}