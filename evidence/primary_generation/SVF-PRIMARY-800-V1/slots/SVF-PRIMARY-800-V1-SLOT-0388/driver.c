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
    if (root != NULL) {
        if (cJSON_IsObject(root)) {
            cJSON *item = cJSON_GetObjectItemCaseSensitive(root, "action");
            if (cJSON_IsString(item) && (item->valuestring != NULL)) {
                if (strcmp(item->valuestring, "ping") == 0) {
                    cJSON *id = cJSON_GetObjectItemCaseSensitive(root, "id");
                    if (cJSON_IsNumber(id)) {
                        volatile double val = id->valuedouble;
                    }
                } else if (strcmp(item->valuestring, "data") == 0) {
                    cJSON *payload = cJSON_GetObjectItemCaseSensitive(root, "payload");
                    if (cJSON_IsArray(payload)) {
                        cJSON *element = NULL;
                        cJSON_ArrayForEach(element, payload) {
                            if (cJSON_IsBool(element)) {
                                volatile int b = cJSON_IsTrue(element);
                            }
                        }
                    }
                }
            }
        } else if (cJSON_IsArray(root)) {
            cJSON *first = cJSON_GetArrayItem(root, 0);
            if (cJSON_IsNumber(first)) {
                volatile double val = first->valuedouble;
            }
        }
        cJSON_Delete(root);
    }

    free(json_str);
    return 0;
}