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
            if (strcmp(type_field->valuestring, "command") == 0) {
                cJSON *cmd = cJSON_GetObjectItemCaseSensitive(root, "cmd");
                if (cJSON_IsString(cmd)) {
                    volatile size_t len = strlen(cmd->valuestring);
                }
            } else if (strcmp(type_field->valuestring, "data") == 0) {
                cJSON *val = cJSON_GetObjectItemCaseSensitive(root, "value");
                if (cJSON_IsNumber(val)) {
                    volatile double d = val->valuedouble;
                }
            }
        }
    } else if (cJSON_IsArray(root)) {
        cJSON *item = NULL;
        cJSON_ArrayForEach(item, root) {
            if (cJSON_IsBool(item)) {
                volatile int b = cJSON_IsTrue(item);
            }
        }
    }

    cJSON_Delete(root);
    free(json_str);
    return 0;
}