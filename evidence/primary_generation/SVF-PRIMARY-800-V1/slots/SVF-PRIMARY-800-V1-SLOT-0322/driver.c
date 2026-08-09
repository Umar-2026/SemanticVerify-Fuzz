#include <stdint.h>
#include <stddef.h>
#include "cJSON.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size == 0) {
        return 0;
    }

    cJSON *root = cJSON_ParseWithLength((const char *)data, size);
    if (root == NULL) {
        return 0;
    }

    if (cJSON_IsObject(root)) {
        cJSON *item = root->child;
        while (item != NULL) {
            if (cJSON_IsString(item) && item->valuestring != NULL) {
                volatile size_t len = strlen(item->valuestring);
                (void)len;
            } else if (cJSON_IsNumber(item)) {
                volatile double val = item->valuedouble;
                (void)val;
            }
            item = item->next;
        }
    }

    cJSON_Delete(root);
    return 0;
}