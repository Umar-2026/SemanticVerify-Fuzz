#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include "cJSON.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size == 0) {
        return 0;
    }

    char *input = (char *)malloc(size + 1);
    if (!input) {
        return 0;
    }
    memcpy(input, data, size);
    input[size] = '\0';

    cJSON *root = cJSON_Parse(input);
    if (root == NULL) {
        free(input);
        return 0;
    }

    cJSON *item = cJSON_GetObjectItemCaseSensitive(root, "type");
    if (item != NULL) {
        if (cJSON_IsString(item)) {
            const char *type_str = item->valuestring;
            if (type_str != NULL) {
                if (strcmp(type_str, "number") == 0) {
                    cJSON *num = cJSON_GetObjectItemCaseSensitive(root, "value");
                    if (num != NULL && cJSON_IsNumber(num)) {
                        double val = num->valuedouble;
                        if (val > 100.0) {
                            // Simulate a functional outcome
                            volatile int result = 1;
                            (void)result;
                        }
                    }
                } else if (strcmp(type_str, "string") == 0) {
                    cJSON *str = cJSON_GetObjectItemCaseSensitive(root, "value");
                    if (str != NULL && cJSON_IsString(str)) {
                        const char *s = str->valuestring;
                        if (s != NULL && strlen(s) > 10) {
                            // Simulate another functional outcome
                            volatile int result = 2;
                            (void)result;
                        }
                    }
                } else if (strcmp(type_str, "array") == 0) {
                    cJSON *arr = cJSON_GetObjectItemCaseSensitive(root, "value");
                    if (arr != NULL && cJSON_IsArray(arr)) {
                        int count = cJSON_GetArraySize(arr);
                        if (count > 5) {
                            // Simulate a third outcome
                            volatile int result = 3;
                            (void)result;
                        }
                    }
                }
            }
        }
    }

    cJSON_Delete(root);
    free(input);
    return 0;
}