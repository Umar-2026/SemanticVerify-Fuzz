#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include "cJSON.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size == 0) return 0;

    char *input = (char *)malloc(size + 1);
    if (!input) return 0;
    memcpy(input, data, size);
    input[size] = '\0';

    cJSON *root = cJSON_Parse(input);
    if (root == NULL) {
        free(input);
        return 0;
    }

    cJSON *item = cJSON_GetObjectItemCaseSensitive(root, "type");
    if (item != NULL && cJSON_IsString(item)) {
        const char *type = item->valuestring;
        if (type != NULL) {
            if (strcmp(type, "number") == 0) {
                cJSON *num = cJSON_GetObjectItemCaseSensitive(root, "value");
                if (num != NULL && cJSON_IsNumber(num)) {
                    double v = num->valuedouble;
                    if (v > 100.0) {
                        // Simulate a functional outcome
                        volatile double result = v * 2.0;
                        (void)result;
                    }
                }
            } else if (strcmp(type, "string") == 0) {
                cJSON *str = cJSON_GetObjectItemCaseSensitive(root, "value");
                if (str != NULL && cJSON_IsString(str)) {
                    const char *s = str->valuestring;
                    if (s != NULL && strlen(s) > 10) {
                        // Simulate another outcome
                        volatile size_t len = strlen(s);
                        (void)len;
                    }
                }
            } else if (strcmp(type, "array") == 0) {
                cJSON *arr = cJSON_GetObjectItemCaseSensitive(root, "value");
                if (arr != NULL && cJSON_IsArray(arr)) {
                    int count = cJSON_GetArraySize(arr);
                    if (count > 5) {
                        // Simulate array outcome
                        volatile int c = count;
                        (void)c;
                    }
                }
            }
        }
    }

    cJSON_Delete(root);
    free(input);
    return 0;
}