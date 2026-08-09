#include <stdint.h>
#include <stddef.h>
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

    if (cJSON_IsObject(root)) {
        cJSON *type_field = cJSON_GetObjectItemCaseSensitive(root, "type");
        if (cJSON_IsString(type_field) && (type_field->valuestring != NULL)) {
            if (strcmp(type_field->valuestring, "action") == 0) {
                cJSON *val = cJSON_GetObjectItemCaseSensitive(root, "value");
                if (cJSON_IsNumber(val)) {
                    volatile double v = val->valuedouble;
                    (void)v;
                }
            } else if (strcmp(type_field->valuestring, "list") == 0) {
                cJSON *items = cJSON_GetObjectItemCaseSensitive(root, "items");
                if (cJSON_IsArray(items)) {
                    cJSON *element = NULL;
                    cJSON_ArrayForEach(element, items) {
                        if (cJSON_IsString(element)) {
                            volatile size_t len = strlen(element->valuestring);
                            (void)len;
                        }
                    }
                }
            }
        }
    } else if (cJSON_IsArray(root)) {
        cJSON *first = cJSON_GetArrayItem(root, 0);
        if (cJSON_IsBool(first)) {
            volatile int b = cJSON_IsTrue(first);
            (void)b;
        }
    }

    cJSON_Delete(root);
    free(json_str);
    return 0;
}