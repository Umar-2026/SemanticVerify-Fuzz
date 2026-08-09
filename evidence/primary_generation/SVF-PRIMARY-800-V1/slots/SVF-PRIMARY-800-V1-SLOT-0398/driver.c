#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "cJSON.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) {
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

    if (cJSON_IsObject(root)) {
        cJSON *new_item = cJSON_CreateString("fuzzed_value");
        if (new_item) {
            cJSON_AddItemToObject(root, "fuzzed_key", new_item);
        }
    }

    char *out = cJSON_PrintUnformatted(root);
    if (out != NULL) {
        free(out);
    }

    cJSON_Delete(root);
    free(json_str);

    return 0;
}