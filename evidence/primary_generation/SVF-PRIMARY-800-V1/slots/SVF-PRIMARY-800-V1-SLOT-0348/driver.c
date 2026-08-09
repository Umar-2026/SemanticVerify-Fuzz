#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "cJSON.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1) {
        return 0;
    }

    char *json_str = (char *)malloc(size + 1);
    if (!json_str) {
        return 0;
    }
    memcpy(json_str, data, size);
    json_str[size] = '\0';

    cJSON *root = cJSON_Parse(json_str);
    if (root == NULL) {
        free(json_str);
        return 0;
    }

    /* Transformation 1: Print the tree to a string (serialization) */
    char *printed = cJSON_Print(root);
    if (printed != NULL) {
        cJSON_free(printed);
    }

    /* Transformation 2: Query the tree for a specific key if it is an object */
    if (cJSON_IsObject(root)) {
        cJSON *item = cJSON_GetObjectItem(root, "fuzz_key");
        if (item != NULL) {
            cJSON_GetArraySize(item);
        }
    }

    cJSON_Delete(root);
    free(json_str);

    return 0;
}