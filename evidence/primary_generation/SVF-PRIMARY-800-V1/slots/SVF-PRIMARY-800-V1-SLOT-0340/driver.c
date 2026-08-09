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
        if (cJSON_IsArray(root)) {
            cJSON *element = NULL;
            cJSON_ArrayForEach(element, root) {
                if (cJSON_IsObject(element)) {
                    cJSON *child = NULL;
                    cJSON_ArrayForEach(child, element) {
                        (void)child->string;
                    }
                }
            }
        } else if (cJSON_IsObject(root)) {
            cJSON *element = NULL;
            cJSON_ArrayForEach(element, root) {
                if (cJSON_IsArray(element)) {
                    cJSON *sub_element = NULL;
                    cJSON_ArrayForEach(sub_element, element) {
                        (void)sub_element->valueint;
                    }
                }
            }
        }
        cJSON_Delete(root);
    }

    free(json_str);
    return 0;
}