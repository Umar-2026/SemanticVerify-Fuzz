#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include "cJSON.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size == 0) {
        return 0;
    }

    // Ensure input is null-terminated for cJSON_Parse
    char *json_str = (char *)malloc(size + 1);
    if (!json_str) {
        return 0;
    }
    memcpy(json_str, data, size);
    json_str[size] = '\0';

    cJSON *root = cJSON_Parse(json_str);
    free(json_str);
    if (root == NULL) {
        return 0;
    }

    // First transformation: count the number of items in the tree
    int count = 0;
    cJSON *item = root;
    while (item) {
        count++;
        item = item->next;
    }

    // Second transformation: find the first string value and print its length
    cJSON *current = root;
    while (current) {
        if (cJSON_IsString(current) && current->valuestring != NULL) {
            // Use the string length as a derived query result
            size_t len = strlen(current->valuestring);
            // Ensure the length is used to avoid optimization
            if (len > 1000000) {
                // This branch is unlikely, but keeps the variable used
                cJSON_Delete(root);
                return 0;
            }
            break;
        }
        current = current->next;
    }

    // Clean up
    cJSON_Delete(root);
    return 0;
}