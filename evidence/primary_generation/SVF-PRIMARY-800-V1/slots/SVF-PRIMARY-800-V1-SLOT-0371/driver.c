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
    unsigned int count = 0;
    if (size > 0) {
        count = data[offset++] % 8; // up to 7 items
    }

    for (unsigned int i = 0; i < count && offset < size; i++) {
        uint8_t type = data[offset++];
        cJSON *item = NULL;

        switch (type % 3) {
            case 0: {
                // Create a child object with a fuzz-derived key and value
                cJSON *child = cJSON_CreateObject();
                if (child == NULL) break;
                char key[16];
                size_t key_len = (size - offset) < 15 ? (size - offset) : 15;
                for (size_t j = 0; j < key_len; j++) {
                    key[j] = (char)(data[offset + j] % 95 + 32);
                }
                key[key_len] = '\0';
                offset += key_len;

                double val = 0.0;
                if (offset + 8 <= size) {
                    memcpy(&val, data + offset, 8);
                    offset += 8;
                }
                cJSON_AddItemToObject(child, key, cJSON_CreateNumber(val));
                cJSON_AddItemToArray(array, child);
                break;
            }
            case 1: {
                // Create a nested array with a number
                cJSON *nested = cJSON_CreateArray();
                if (nested == NULL) break;
                double val = 0.0;
                if (offset + 8 <= size) {
                    memcpy(&val, data + offset, 8);
                    offset += 8;
                }
                cJSON_AddItemToArray(nested, cJSON_CreateNumber(val));
                cJSON_AddItemToArray(array, nested);
                break;
            }
            case 2: {
                // Create a string item
                size_t str_len = (size - offset) < 20 ? (size - offset) : 20;
                char *str = (char *)malloc(str_len + 1);
                if (str == NULL) break;
                for (size_t j = 0; j < str_len; j++) {
                    str[j] = (char)(data[offset + j] % 95 + 32);
                }
                str[str_len] = '\0';
                offset += str_len;
                cJSON *str_item = cJSON_CreateString(str);
                free(str);
                if (str_item != NULL) {
                    cJSON_AddItemToArray(array, str_item);
                }
                break;
            }
        }
    }

    cJSON_Delete(root);
    return 0;
}