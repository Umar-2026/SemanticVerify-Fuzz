#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include "cJSON.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) {
        return 0;
    }

    // Use the first byte to determine the modification type
    uint8_t mod_type = data[0];
    // Use the second byte as a parameter for the modification
    uint8_t mod_param = data[1];

    // The rest of the input is the JSON document
    const char *json_str = (const char *)(data + 2);
    size_t json_len = size - 2;

    // Ensure the JSON string is null-terminated
    char *json_copy = (char *)malloc(json_len + 1);
    if (!json_copy) {
        return 0;
    }
    memcpy(json_copy, json_str, json_len);
    json_copy[json_len] = '\0';

    cJSON *root = cJSON_Parse(json_copy);
    free(json_copy);

    if (root == NULL) {
        return 0;
    }

    // Apply a fuzz-derived modification to the tree
    switch (mod_type % 4) {
        case 0: {
            // Modify a string value if present
            cJSON *item = root;
            if (cJSON_IsString(item)) {
                char *new_str = (char *)malloc(mod_param + 1);
                if (new_str) {
                    memset(new_str, 'A' + (mod_param % 26), mod_param);
                    new_str[mod_param] = '\0';
                    if (cJSON_SetValuestring(item, new_str) == NULL) {
                        free(new_str);
                    } else {
                        free(new_str);
                    }
                }
            }
            break;
        }
        case 1: {
            // Change a number value if present
            cJSON *item = root;
            if (cJSON_IsNumber(item)) {
                item->valuedouble = (double)mod_param;
                item->valueint = mod_param;
            }
            break;
        }
        case 2: {
            // Toggle a boolean value if present
            cJSON *item = root;
            if (cJSON_IsBool(item)) {
                item->type = (item->type == cJSON_True) ? cJSON_False : cJSON_True;
            }
            break;
        }
        case 3: {
            // Add a new item to an object or array if present
            if (cJSON_IsObject(root) || cJSON_IsArray(root)) {
                char key[16];
                snprintf(key, sizeof(key), "k%d", mod_param);
                cJSON *new_item = cJSON_CreateNumber((double)mod_param);
                if (new_item) {
                    if (cJSON_IsObject(root)) {
                        cJSON_AddItemToObject(root, key, new_item);
                    } else {
                        cJSON_AddItemToArray(root, new_item);
                    }
                }
            }
            break;
        }
    }

    // Serialize the modified tree
    char *printed = cJSON_PrintUnformatted(root);
    if (printed) {
        free(printed);
    }

    cJSON_Delete(root);
    return 0;
}