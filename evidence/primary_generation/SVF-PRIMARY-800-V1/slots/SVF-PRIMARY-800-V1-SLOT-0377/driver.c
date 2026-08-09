#include <stdint.h>
#include <stddef.h>
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

    cJSON *array = cJSON_CreateArray();
    if (array == NULL) {
        cJSON_Delete(root);
        return 0;
    }

    cJSON_AddItemToObject(root, "items", array);

    size_t offset = 0;
    size_t num_children = data[offset++] % 8;  // 0 to 7 children
    if (offset + num_children > size) {
        cJSON_Delete(root);
        return 0;
    }

    for (size_t i = 0; i < num_children; i++) {
        uint8_t type = data[offset++];
        cJSON *child = NULL;

        switch (type % 4) {
            case 0: {
                // Create a child object with a fuzz-derived key and value
                if (offset + 2 > size) {
                    cJSON_Delete(root);
                    return 0;
                }
                uint8_t key_len = data[offset] % 16;
                offset++;
                if (offset + key_len > size) {
                    cJSON_Delete(root);
                    return 0;
                }
                char *key = (char *)malloc(key_len + 1);
                if (key == NULL) {
                    cJSON_Delete(root);
                    return 0;
                }
                memcpy(key, data + offset, key_len);
                key[key_len] = '\0';
                offset += key_len;

                uint8_t val_type = data[offset++];
                cJSON *val = NULL;
                if (val_type % 2 == 0) {
                    val = cJSON_CreateNumber((double)(data[offset] % 100));
                } else {
                    if (offset + 1 > size) {
                        free(key);
                        cJSON_Delete(root);
                        return 0;
                    }
                    uint8_t str_len = data[offset] % 16;
                    offset++;
                    if (offset + str_len > size) {
                        free(key);
                        cJSON_Delete(root);
                        return 0;
                    }
                    char *str = (char *)malloc(str_len + 1);
                    if (str == NULL) {
                        free(key);
                        cJSON_Delete(root);
                        return 0;
                    }
                    memcpy(str, data + offset, str_len);
                    str[str_len] = '\0';
                    offset += str_len;
                    val = cJSON_CreateString(str);
                    free(str);
                }
                if (val == NULL) {
                    free(key);
                    cJSON_Delete(root);
                    return 0;
                }
                child = cJSON_CreateObject();
                if (child == NULL) {
                    cJSON_Delete(val);
                    free(key);
                    cJSON_Delete(root);
                    return 0;
                }
                cJSON_AddItemToObject(child, key, val);
                free(key);
                break;
            }
            case 1: {
                // Create a number child
                if (offset + 1 > size) {
                    cJSON_Delete(root);
                    return 0;
                }
                child = cJSON_CreateNumber((double)(data[offset] % 1000));
                offset++;
                break;
            }
            case 2: {
                // Create a string child
                if (offset + 1 > size) {
                    cJSON_Delete(root);
                    return 0;
                }
                uint8_t str_len = data[offset] % 16;
                offset++;
                if (offset + str_len > size) {
                    cJSON_Delete(root);
                    return 0;
                }
                char *str = (char *)malloc(str_len + 1);
                if (str == NULL) {
                    cJSON_Delete(root);
                    return 0;
                }
                memcpy(str, data + offset, str_len);
                str[str_len] = '\0';
                offset += str_len;
                child = cJSON_CreateString(str);
                free(str);
                break;
            }
            case 3: {
                // Create a boolean child
                child = cJSON_CreateBool(data[offset] % 2);
                offset++;
                break;
            }
            default:
                child = NULL;
                break;
        }

        if (child != NULL) {
            cJSON_AddItemToArray(array, child);
        } else {
            cJSON_Delete(root);
            return 0;
        }
    }

    cJSON_Delete(root);
    return 0;
}