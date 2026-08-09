#include <stdlib.h>
#include <string.h>
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
    free(json_str);
    if (root == NULL) {
        return 0;
    }

    cJSON *item = cJSON_GetObjectItemCaseSensitive(root, "type");
    if (item != NULL) {
        if (cJSON_IsString(item) && (item->valuestring != NULL)) {
            if (strcmp(item->valuestring, "number") == 0) {
                cJSON *num = cJSON_GetObjectItemCaseSensitive(root, "value");
                if (cJSON_IsNumber(num)) {
                    volatile double d = num->valuedouble;
                    (void)d;
                }
            } else if (strcmp(item->valuestring, "string") == 0) {
                cJSON *str = cJSON_GetObjectItemCaseSensitive(root, "value");
                if (cJSON_IsString(str) && (str->valuestring != NULL)) {
                    volatile size_t len = strlen(str->valuestring);
                    (void)len;
                }
            } else if (strcmp(item->valuestring, "array") == 0) {
                cJSON *arr = cJSON_GetObjectItemCaseSensitive(root, "value");
                if (cJSON_IsArray(arr)) {
                    volatile int count = cJSON_GetArraySize(arr);
                    (void)count;
                }
            }
        }
    }

    cJSON_Delete(root);
    return 0;
}