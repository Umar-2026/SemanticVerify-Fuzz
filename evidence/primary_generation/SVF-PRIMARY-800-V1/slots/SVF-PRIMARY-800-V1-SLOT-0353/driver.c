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
        if (offset + name_len > size) {
            break;
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
        switch (type % 6) {
            case 0: {
                if (offset + sizeof(int) > size) {
                    free(name);
                    cJSON_Delete(root);
                    return 0;
                }
                int val;
                memcpy(&val, data + offset, sizeof(int));
                offset += sizeof(int);
                item = cJSON_CreateNumber((double)val);
                break;
            }
            case 1: {
                if (offset + sizeof(double) > size) {
                    free(name);
                    cJSON_Delete(root);
                    return 0;
                }
                double val;
                memcpy(&val, data + offset, sizeof(double));
                offset += sizeof(double);
                item = cJSON_CreateNumber(val);
                break;
            }
            case 2: {
                if (offset >= size) {
                    free(name);
                    cJSON_Delete(root);
                    return 0;
                }
                uint8_t bool_val = data[offset++];
                item = cJSON_CreateBool(bool_val & 1);
                break;
            }
            case 3: {
                if (offset >= size) {
                    free(name);
                    cJSON_Delete(root);
                    return 0;
                }
                uint8_t null_val = data[offset++];
                (void)null_val;
                item = cJSON_CreateNull();
                break;
            }
            case 4: {
                if (offset >= size) {
                    free(name);
                    cJSON_Delete(root);
                    return 0;
                }
                size_t str_len = data[offset++];
                if (offset + str_len > size) {
                    free(name);
                    cJSON_Delete(root);
                    return 0;
                }
                char *str = (char *)malloc(str_len + 1);
                if (str == NULL) {
                    free(name);
                    cJSON_Delete(root);
                    return 0;
                }
                memcpy(str, data + offset, str_len);
                str[str_len] = '\0';
                offset += str_len;
                item = cJSON_CreateString(str);
                free(str);
                break;
            }
            case 5: {
                item = cJSON_CreateArray();
                if (item != NULL) {
                    size_t arr_count = data[offset++];
                    for (size_t i = 0; i < arr_count && offset < size; i++) {
                        cJSON *child = cJSON_CreateNumber((double)data[offset++]);
                        if (child != NULL) {
                            cJSON_AddItemToArray(item, child);
                        }
                    }
                }
                break;
            }
        }

        if (item != NULL) {
            cJSON_AddItemToObject(root, name, item);
        }
        free(name);
    }

    cJSON_Delete(root);
    return 0;
}