#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include "cJSON.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) {
        return 0;
    }

    cJSON *root = cJSON_CreateObject();
    if (root == NULL) {
        return 0;
    }

    size_t offset = 0;
    while (offset + 2 <= size) {
        uint8_t type = data[offset] % 4;
        uint8_t key_len = data[offset + 1];
        offset += 2;

        if (offset + key_len > size) {
            break;
        }

        char *key = (char *)malloc(key_len + 1);
        if (key == NULL) {
            cJSON_Delete(root);
            return 0;
        }
        memcpy(key, data + offset, key_len);
        key[key_len] = '\0';
        offset += key_len;

        cJSON *item = NULL;
        switch (type) {
            case 0: {
                if (offset + sizeof(int) <= size) {
                    int val;
                    memcpy(&val, data + offset, sizeof(int));
                    offset += sizeof(int);
                    item = cJSON_CreateNumber((double)val);
                }
                break;
            }
            case 1: {
                if (offset + 1 <= size) {
                    item = cJSON_CreateBool(data[offset] % 2);
                    offset += 1;
                }
                break;
            }
            case 2: {
                if (offset + 1 <= size) {
                    uint8_t str_len = data[offset];
                    offset += 1;
                    if (offset + str_len <= size) {
                        char *str = (char *)malloc(str_len + 1);
                        if (str != NULL) {
                            memcpy(str, data + offset, str_len);
                            str[str_len] = '\0';
                            offset += str_len;
                            item = cJSON_CreateString(str);
                            free(str);
                        }
                    }
                }
                break;
            }
            case 3: {
                item = cJSON_CreateNull();
                break;
            }
            default:
                break;
        }

        if (item != NULL) {
            cJSON_AddItemToObject(root, key, item);
        }

        free(key);

        if (offset >= size) {
            break;
        }
    }

    cJSON_Delete(root);
    return 0;
}