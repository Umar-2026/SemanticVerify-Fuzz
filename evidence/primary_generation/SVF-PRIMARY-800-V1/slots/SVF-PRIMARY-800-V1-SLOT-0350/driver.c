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

    if (cJSON_IsObject(root)) {
        cJSON *child = root->child;
        while (child != NULL) {
            char *name = child->string;
            if (name != NULL) {
                size_t len = strlen(name);
                (void)len;
            }
            child = child->next;
        }
    }

    char *rendered = cJSON_PrintUnformatted(root);
    if (rendered != NULL) {
        size_t rendered_len = strlen(rendered);
        (void)rendered_len;
        free(rendered);
    }

    cJSON_Delete(root);
    free(json_str);

    return 0;
}