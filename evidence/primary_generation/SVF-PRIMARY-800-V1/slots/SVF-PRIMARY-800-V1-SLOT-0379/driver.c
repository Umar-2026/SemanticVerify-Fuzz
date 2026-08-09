#include <stdint.h>
#include <stddef.h>
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

    cJSON *array = cJSON_CreateArray();
    if (array == NULL) {
        cJSON_Delete(root);
        return 0;
    }

    cJSON_AddItemToObject(root, "items", array);

    size_t offset = 0;
    size_t num_items = data[offset] % 8;
    offset++;
    if (offset >= size) {
        cJSON_Delete(root);
        return 0;
    }

    for (size_t i = 0; i < num_items && offset < size; i++) {
        uint8_t type = data[offset] % 3;
        offset++;
        if (offset >= size) {
            break;
        }

        cJSON *item = NULL;
        switch (type) {
            case 0: {
                size_t len = data[offset] % 16;
                offset++;
                if (offset + len > size) {
                    len = size - offset;
                }
                char *str = (char *)malloc(len + 1);
                if (str == NULL) {
                    cJSON_Delete(root);
                    return 0;
                }
                memcpy(str, data + offset, len);
                str[len] = '\0';
                offset += len;
                item = cJSON_CreateString(str);
                free(str);
                break;
            }
            case 1: {
                if (offset + sizeof(int) > size) {
                    offset = size;
                    break;
                }
                int val;
                memcpy(&val, data + offset, sizeof(int));
                offset += sizeof(int);
                item = cJSON_CreateNumber((double)val);
                break;
            }
            case 2: {
                item = cJSON_CreateBool(data[offset] % 2);
                offset++;
                break;
            }
            default:
                break;
        }

        if (item != NULL) {
            cJSON_AddItemToArray(array, item);
        }
    }

    cJSON_Delete(root);
    return 0;
}