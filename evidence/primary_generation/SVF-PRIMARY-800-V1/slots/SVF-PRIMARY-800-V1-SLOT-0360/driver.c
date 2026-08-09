#include <stdint.h>
#include <stdlib.h>
#include "cJSON.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 4) {
        return 0;
    }

    cJSON *root = cJSON_CreateObject();
    if (root == NULL) {
        return 0;
    }

    size_t offset = 0;
    while (offset + 2 < size) {
        size_t key_len = data[offset] % (size - offset - 1);
        offset++;
        
        char *key = (char *)malloc(key_len + 1);
        if (!key) break;
        
        for (size_t i = 0; i < key_len; i++) {
            key[i] = (data[offset + i] % 94) + 32;
        }
        key[key_len] = '\0';
        offset += key_len;

        cJSON *val = cJSON_CreateNumber((double)data[offset]);
        offset++;

        if (val) {
            cJSON_AddItemToObject(root, key, val);
        }
        
        free(key);
    }

    cJSON_Delete(root);
    return 0;
}