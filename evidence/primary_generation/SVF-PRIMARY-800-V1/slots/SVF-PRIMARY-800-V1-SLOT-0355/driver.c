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

        size_t name_len = data[offset++];
        if (name_len > size - offset) {
            name_len = size - offset;
        }
        char *name = (char *)malloc(name_len + 1);
        if (name == NULL) {
            cJSON_Delete(root);
            return 0;
        }
        memcpy(name, data + offset, name_len);
        name[name_len] = '\0';
        offset += name_len;

        cJSON *item = NULL;
        switch (type % 5) {
            case 0: {
                if (offset < size) {
                    item = cJSON_CreateNumber((double)(data[offset] - 128));
                    offset++;
                }
                break;
            }
            case 1: {
                if (offset < size) {
                    item = cJSON_CreateBool(data[offset] % 2);
                    offset++;
                }
                break;
            }
            case 2: {
                if (offset < size) {
                    size_t str_len = data[offset++];
                    if (str_len > size - offset) {
                        str_len = size - offset;
                    }
                    char *str = (char *)malloc(str_len + 1);
                    if (str != NULL) {
                        memcpy(str, data + offset, str_len);
                        str[str_len] = '\0';
                        item = cJSON_CreateString(str);
                        free(str);
                        offset += str_len;
                    }
                }
                break;
            }
            case 3: {
                item = cJSON_CreateNull();
                break;
            }
            case 4: {
                item = cJSON_CreateObject();
                break;
            }
            default:
                break;
        }

        if (item != NULL) {
            cJSON_AddItemToObject(root, name, item);
        }
        free(name);

        if (offset >= size) {
            break;
        }
    }

    cJSON_Delete(root);
    return 0;
}