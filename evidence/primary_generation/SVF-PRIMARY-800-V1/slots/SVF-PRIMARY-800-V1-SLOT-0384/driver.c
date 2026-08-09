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
        cJSON *item = cJSON_GetObjectItemCaseSensitive(root, "type");
        if (cJSON_IsString(item) && (item->valuestring != NULL)) {
            if (strcmp(item->valuestring, "action") == 0) {
                cJSON *val = cJSON_GetObjectItemCaseSensitive(root, "value");
                if (cJSON_IsNumber(val)) {
                    volatile double d = val->valuedouble;
                    (void)d;
                }
            } else if (strcmp(item->valuestring, "status") == 0) {
                cJSON *flag = cJSON_GetObjectItemCaseSensitive(root, "enabled");
                if (cJSON_IsBool(flag)) {
                    volatile int b = cJSON_IsTrue(flag);
                    (void)b;
                }
            }
        }
    } else if (cJSON_IsArray(root)) {
        cJSON *element = NULL;
        cJSON_ArrayForEach(element, root) {
            if (cJSON_IsNumber(element)) {
                volatile double d = element->valuedouble;
                (void)d;
            }
        }
    }

    cJSON_Delete(root);
    free(json_str);
    return 0;
}