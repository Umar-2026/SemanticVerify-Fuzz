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
    // Use the second byte to determine the index for modification
    uint8_t mod_index = data[1];

    // The rest of the data is the JSON document
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
    // We'll traverse the tree and modify a node based on mod_type and mod_index
    // For simplicity, we'll modify the first string value we find, or add a new key if none exists
    cJSON *node = root;
    int index = 0;
    int found = 0;

    // Simple recursive traversal to find a node to modify
    // We'll use a stack-based approach to avoid recursion depth issues
    // But for simplicity, we'll just iterate through the root's children if it's an object or array
    if (cJSON_IsObject(root) || cJSON_IsArray(root)) {
        cJSON *child = root->child;
        while (child != NULL) {
            if (index == mod_index) {
                node = child;
                found = 1;
                break;
            }
            index++;
            child = child->next;
        }
    }

    if (!found) {
        // If no node found at that index, just add a new item to the root if it's an object
        if (cJSON_IsObject(root)) {
            char key[2] = {0};
            key[0] = 'a' + (mod_index % 26);
            cJSON_AddItemToObject(root, key, cJSON_CreateNumber((double)mod_type));
        } else if (cJSON_IsArray(root)) {
            cJSON_AddItemToArray(root, cJSON_CreateNumber((double)mod_type));
        }
    } else {
        // Modify the found node based on mod_type
        switch (mod_type % 4) {
            case 0:
                // Change to a number
                if (cJSON_IsString(node)) {
                    cJSON *replacement = cJSON_CreateNumber((double)mod_index);
                    if (replacement) {
                        if (node->string) {
                            cJSON_ReplaceItemInObject(root, node->string, replacement);
                        } else {
                            // For array items, we need to replace in place
                            // cJSON doesn't have a direct replace for array items, so we'll just delete and add
                            // But for simplicity, we'll just change the value type
                            // Actually, we can just set the value
                            // We'll just change the node's type and value
                            // This is hacky but works for the fuzzer
                            node->type = cJSON_Number;
                            node->valuedouble = (double)mod_index;
                            node->valueint = mod_index;
                        }
                    }
                }
                break;
            case 1:
                // Change to a string
                if (cJSON_IsNumber(node)) {
                    char buf[32];
                    snprintf(buf, sizeof(buf), "fuzz_%d", mod_index);
                    cJSON *replacement = cJSON_CreateString(buf);
                    if (replacement) {
                        if (node->string) {
                            cJSON_ReplaceItemInObject(root, node->string, replacement);
                        } else {
                            node->type = cJSON_String;
                            node->valuestring = strdup(buf);
                        }
                    }
                }
                break;
            case 2:
                // Change to a boolean
                if (cJSON_IsNumber(node) || cJSON_IsString(node)) {
                    node->type = cJSON_True;
                }
                break;
            case 3:
                // Change to null
                if (cJSON_IsNumber(node) || cJSON_IsString(node)) {
                    node->type = cJSON_NULL;
                }
                break;
        }
    }

    // Serialize the modified tree
    char *output = cJSON_PrintUnformatted(root);
    if (output) {
        free(output);
    }

    cJSON_Delete(root);
    return 0;
}