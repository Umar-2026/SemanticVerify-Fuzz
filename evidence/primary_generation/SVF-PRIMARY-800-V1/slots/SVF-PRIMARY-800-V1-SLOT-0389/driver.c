#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include "cJSON.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size == 0) {
        return 0;
    }

    char *json_str = (char *)malloc(size + 1);
    if (!json_str) {
        return 0;
    }
    memcpy(json_str, data, size);
    json_str[size] = '\0';

    cJSON *root = cJSON_Parse(json_str);
    if (root == NULL) {
        free(json_str);
        return 0;
    }

    cJSON *item = cJSON_GetObjectItemCaseSensitive(root, "type");
    if (item != NULL) {
        if (cJSON_IsString(item)) {
            const char *type_str = item->valuestring;
            if (type_str != NULL) {
                if (strcmp(type_str, "number") == 0) {
                    cJSON *num_item = cJSON_GetObjectItemCaseSensitive(root, "value");
                    if (num_item != NULL && cJSON_IsNumber(num_item)) {
                        double val = num_item->valuedouble;
                        if (val > 100.0) {
                            // High value path
                        } else {
                            // Low value path
                        }
                    }
                } else if (strcmp(type_str, "string") == 0) {
                    cJSON *str_item = cJSON_GetObjectItemCaseSensitive(root, "value");
                    if (str_item != NULL && cJSON_IsString(str_item)) {
                        const char *str_val = str_item->valuestring;
                        if (str_val != NULL && strlen(str_val) > 10) {
                            // Long string path
                        } else {
                            // Short string path
                        }
                    }
                } else if (strcmp(type_str, "array") == 0) {
                    cJSON *arr_item = cJSON_GetObjectItemCaseSensitive(root, "value");
                    if (arr_item != NULL && cJSON_IsArray(arr_item)) {
                        int count = cJSON_GetArraySize(arr_item);
                        if (count > 5) {
                            // Large array path
                        } else {
                            // Small array path
                        }
                    }
                }
            }
        } else if (cJSON_IsNumber(item)) {
            double type_num = item->valuedouble;
            if (type_num > 0) {
                // Positive type number path
            } else {
                // Non-positive type number path
            }
        }
    }

    cJSON_Delete(root);
    free(json_str);
    return 0;
}