#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include "cJSON.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1) {
        return 0;
    }

    cJSON *root = cJSON_CreateObject();
    if (root == NULL) {
        return 0;
    }

    size_t offset = 0;
    while (offset < size) {
        uint8_t type = data[offset++];
        if (offset >= size) {
            break;
        }

        size_t key_len = data[offset++];
        if (key_len > size - offset) {
            key_len = size - offset;
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
        switch (type % 4) {
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
                if (offset + sizeof(double) <= size) {
                    double val;
                    memcpy(&val, data + offset, sizeof(double));
                    offset += sizeof(double);
                    item = cJSON_CreateNumber(val);
                }
                break;
            }
            case 2: {
                if (offset < size) {
                    uint8_t bool_val = data[offset++];
                    item = cJSON_CreateBool(bool_val & 1);
                }
                break;
            }
            case 3: {
                if (offset < size) {
                    size_t str_len = data[offset++];
                    if (str_len > size - offset) {
                        str_len = size - offset;
                    }
                    char *str = (char *)malloc(str_len + 1);
                    if (str != NULL) {
                        memcpy(str, data + offset, str_len);
                        str[str_len] = '\0';
                        offset += str_len;
                        item = cJSON_CreateString(str);
                        free(str);
                    }
                }
                break;
            }
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