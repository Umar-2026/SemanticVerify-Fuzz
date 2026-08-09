#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "cJSON.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1) {
        return 0;
    }

    char *json_str = (char *)malloc(size + 1);
    if (json_str == NULL) {
        return 0;
    }
    memcpy(json_str, data, size);
    json_str[size] = '\0';

    cJSON *root = cJSON_Parse(json_str);
    if (root == NULL) {
        free(json_str);
        return 0;
    }

    // Transformation 1: Print the JSON to a string (serialization)
    char *printed = cJSON_Print(root);
    if (printed != NULL) {
        cJSON_free(printed);
    }

    // Transformation 2: Query the root for a specific key or type
    // We perform a generic traversal/query to ensure the tree is navigated
    if (cJSON_IsObject(root)) {
        cJSON *child = root->child;
        while (child != NULL) {
            const char *name = child->string;
            if (name != NULL) {
                cJSON *item = cJSON_GetObjectItem(root, name);
                (void)item;
            }
            child = child->next;
        }
    } else if (cJSON_IsArray(root)) {
        int array_size = cJSON_GetArraySize(root);
        if (array_size > 0) {
            cJSON *first = cJSON_GetArrayItem(root, 0);
            (void)first;
        }
    }

    cJSON_Delete(root);
    free(json_str);

    return 0;
}