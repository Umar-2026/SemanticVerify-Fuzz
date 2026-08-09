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
    // Use the second byte to determine the path depth or index
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

    // Apply a modification based on mod_type
    switch (mod_type % 4) {
        case 0: {
            // Delete a child at a given index (if array) or by name (if object)
            if (cJSON_IsArray(root)) {
                int index = mod_param % cJSON_GetArraySize(root);
                cJSON_DeleteItemFromArray(root, index);
            } else if (cJSON_IsObject(root)) {
                // Use the mod_param to pick a child by index
                int index = mod_param % cJSON_GetArraySize(root);
                cJSON *child = cJSON_GetArrayItem(root, index);
                if (child && child->string) {
                    cJSON_DeleteItemFromObject(root, child->string);
                }
            }
            break;
        }
        case 1: {
            // Add a new number item
            cJSON *num = cJSON_CreateNumber((double)mod_param);
            if (num) {
                if (cJSON_IsArray(root)) {
                    cJSON_AddItemToArray(root, num);
                } else if (cJSON_IsObject(root)) {
                    char name[16];
                    snprintf(name, sizeof(name), "fuzz_%u", mod_param);
                    cJSON_AddItemToObject(root, name, num);
                } else {
                    cJSON_Delete(num);
                }
            }
            break;
        }
        case 2: {
            // Modify a value at a given index
            int index = mod_param % cJSON_GetArraySize(root);
            cJSON *item = cJSON_GetArrayItem(root, index);
            if (item) {
                if (cJSON_IsString(item)) {
                    char *new_str = (char *)malloc(32);
                    if (new_str) {
                        snprintf(new_str, 32, "modified_%u", mod_param);
                        cJSON_SetValuestring(item, new_str);
                        free(new_str);
                    }
                } else if (cJSON_IsNumber(item)) {
                    item->valuedouble = (double)mod_param;
                    item->valueint = mod_param;
                } else if (cJSON_IsBool(item)) {
                    item->type = (mod_param % 2) ? cJSON_True : cJSON_False;
                }
            }
            break;
        }
        case 3: {
            // Duplicate a child item
            int index = mod_param % cJSON_GetArraySize(root);
            cJSON *item = cJSON_GetArrayItem(root, index);
            if (item) {
                cJSON *dup = cJSON_Duplicate(item, 1);
                if (dup) {
                    if (cJSON_IsArray(root)) {
                        cJSON_AddItemToArray(root, dup);
                    } else if (cJSON_IsObject(root) && item->string) {
                        char new_name[64];
                        snprintf(new_name, sizeof(new_name), "%s_copy", item->string);
                        cJSON_AddItemToObject(root, new_name, dup);
                    } else {
                        cJSON_Delete(dup);
                    }
                }
            }
            break;
        }
    }

    // Serialize the modified tree
    char *out = cJSON_PrintUnformatted(root);
    if (out) {
        free(out);
    }

    cJSON_Delete(root);
    return 0;
}