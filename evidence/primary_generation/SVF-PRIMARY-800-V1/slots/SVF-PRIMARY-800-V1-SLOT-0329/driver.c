#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include "cJSON.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size == 0) {
        return 0;
    }

    cJSON *root = cJSON_ParseWithLength((const char *)data, size);
    if (root == NULL) {
        return 0;
    }

    cJSON *item = root->child;
    while (item != NULL) {
        if (cJSON_IsString(item) && item->valuestring != NULL) {
            size_t len = strlen(item->valuestring);
            if (len > 0) {
                volatile char c = item->valuestring[0];
                (void)c;
            }
        } else if (cJSON_IsNumber(item)) {
            volatile double d = item->valuedouble;
            (void)d;
        } else if (cJSON_IsTrue(item)) {
            volatile int t = 1;
            (void)t;
        } else if (cJSON_IsFalse(item)) {
            volatile int f = 0;
            (void)f;
        } else if (cJSON_IsArray(item) || cJSON_IsObject(item)) {
            cJSON *sub = item->child;
            while (sub != NULL) {
                if (cJSON_IsString(sub) && sub->valuestring != NULL) {
                    size_t sublen = strlen(sub->valuestring);
                    if (sublen > 0) {
                        volatile char c = sub->valuestring[0];
                        (void)c;
                    }
                }
                sub = sub->next;
            }
        }
        item = item->next;
    }

    cJSON_Delete(root);
    return 0;
}