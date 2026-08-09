#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include "cJSON.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1) return 0;

    cJSON *root = cJSON_CreateObject();
    if (root == NULL) return 0;

    cJSON *array = cJSON_CreateArray();
    if (array == NULL) {
        cJSON_Delete(root);
        return 0;
    }

    cJSON_AddItemToObject(root, "items", array);

    size_t offset = 0;
    while (offset < size) {
        uint8_t type = data[offset++];
        cJSON *child = NULL;

        if (type % 3 == 0) {
            child = cJSON_CreateObject();
            if (child != NULL) {
                cJSON *sub = cJSON_CreateObject();
                if (sub != NULL) {
                    cJSON_AddItemToObject(child, "sub", sub);
                }
            }
        } else if (type % 3 == 1) {
            child = cJSON_CreateArray();
            if (child != NULL) {
                cJSON *num = cJSON_CreateNumber((double)(type));
                if (num != NULL) {
                    cJSON_AddItemToArray(child, num);
                }
            }
        } else {
            if (offset < size) {
                uint8_t val = data[offset++];
                child = cJSON_CreateNumber((double)val);
            } else {
                child = cJSON_CreateNull();
            }
        }

        if (child != NULL) {
            cJSON_AddItemToArray(array, child);
        }

        if (offset >= size) break;
    }

    cJSON_Delete(root);
    return 0;
}