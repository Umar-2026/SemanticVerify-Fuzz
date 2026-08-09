#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include "cJSON.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size == 0) {
        return 0;
    }

    // Ensure input is null-terminated for cJSON_Parse
    char *input = (char *)malloc(size + 1);
    if (!input) {
        return 0;
    }
    memcpy(input, data, size);
    input[size] = '\0';

    cJSON *root = cJSON_Parse(input);
    if (root == NULL) {
        free(input);
        return 0;
    }

    // First transformation/query: count the number of items in the tree
    int count = 0;
    cJSON *item = root;
    while (item != NULL) {
        count++;
        item = item->next;
    }

    // Second transformation/query: find the first string value and modify it
    cJSON *first_string = NULL;
    cJSON *current = root;
    while (current != NULL) {
        if (cJSON_IsString(current) && current->valuestring != NULL) {
            first_string = current;
            break;
        }
        current = current->child;
        // Traverse children recursively if needed (simplified: only top-level and first-level children)
        if (current == NULL && first_string == NULL) {
            // Fallback: traverse all children of root
            cJSON *child = root->child;
            while (child != NULL) {
                if (cJSON_IsString(child) && child->valuestring != NULL) {
                    first_string = child;
                    break;
                }
                child = child->next;
            }
        }
    }

    if (first_string != NULL) {
        // Modify the string value (e.g., truncate to first character)
        if (first_string->valuestring[0] != '\0') {
            first_string->valuestring[1] = '\0';
        }
    }

    // Use the count to avoid optimization (e.g., print or just keep it)
    volatile int sink = count;
    (void)sink;

    cJSON_Delete(root);
    free(input);
    return 0;
}