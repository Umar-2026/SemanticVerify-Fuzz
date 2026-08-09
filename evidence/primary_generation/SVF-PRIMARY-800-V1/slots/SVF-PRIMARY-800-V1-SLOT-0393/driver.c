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

    // The rest is the JSON document
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
    cJSON *target = root;
    // Navigate to a child based on mod_param (simple traversal)
    if (mod_param > 0 && cJSON_IsArray(root)) {
        int index = mod_param % cJSON_GetArraySize(root);
        target = cJSON_GetArrayItem(root, index);
        if (target == NULL) {
            cJSON_Delete(root);
            return 0;
        }
    } else if (mod_param > 0 && cJSON_IsObject(root)) {
        // Navigate to the first child if object
        target = root->child;
        if (target == NULL) {
            cJSON_Delete(root);
            return 0;
        }
    }

    // Perform modification based on mod_type
    switch (mod_type % 4) {
        case 0:
            // Change value to a number
            if (cJSON_IsString(target) || cJSON_IsNumber(target)) {
                cJSON_SetNumberValue(target, (double)mod_param);
            }
            break;
        case 1:
            // Change value to a string
            if (cJSON_IsString(target) || cJSON_IsNumber(target)) {
                char buf[16];
                snprintf(buf, sizeof(buf), "%u", mod_param);
                cJSON_SetValuestring(target, buf);
            }
            break;
        case 2:
            // Change value to a boolean
            if (cJSON_IsString(target) || cJSON_IsNumber(target)) {
                cJSON_SetBoolValue(target, mod_param % 2);
            }
            break;
        case 3:
            // Change value to null
            if (cJSON_IsString(target) || cJSON_IsNumber(target)) {
                cJSON_SetNull(target);
            }
            break;
        default:
            break;
    }

    // Serialize the modified tree
    char *out = cJSON_PrintUnformatted(root);
    if (out != NULL) {
        free(out);
    }

    cJSON_Delete(root);
    return 0;
}