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
    // Use the second byte as a parameter (e.g., index or value)
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

    // Apply a fuzz-derived modification to the parsed tree
    switch (mod_type % 4) {
        case 0: {
            // Add a new item to the root if it's an object
            if (cJSON_IsObject(root)) {
                char key[16];
                snprintf(key, sizeof(key), "fuzz_%u", mod_param);
                cJSON *new_item = cJSON_CreateNumber((double)mod_param);
                if (new_item) {
                    cJSON_AddItemToObject(root, key, new_item);
                }
            }
            break;
        }
        case 1: {
            // Remove an item from the root if it's an object
            if (cJSON_IsObject(root) && root->child) {
                cJSON *to_remove = root->child;
                // Walk to the item at index mod_param (bounded by list length)
                for (uint8_t i = 0; i < mod_param && to_remove->next; i++) {
                    to_remove = to_remove->next;
                }
                cJSON_DeleteItemFromObject(root, to_remove->string);
            }
            break;
        }
        case 2: {
            // Modify the value of the first child if it's a number
            if (root->child && cJSON_IsNumber(root->child)) {
                root->child->valuedouble = (double)mod_param;
                root->child->valueint = mod_param;
            }
            break;
        }
        case 3: {
            // Duplicate the root and replace it (then delete the original)
            cJSON *dup = cJSON_Duplicate(root, 1);
            if (dup) {
                cJSON_Delete(root);
                root = dup;
            }
            break;
        }
        default:
            break;
    }

    // Serialize the modified tree
    char *printed = cJSON_PrintUnformatted(root);
    if (printed) {
        free(printed);
    }

    cJSON_Delete(root);
    return 0;
}