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
    free(input);

    if (root == NULL) {
        return 0;
    }

    // First independent query: count the number of items in the root object/array
    int count = 0;
    if (cJSON_IsArray(root) || cJSON_IsObject(root)) {
        cJSON *child = root->child;
        while (child != NULL) {
            count++;
            child = child->next;
        }
    }

    // Second independent query: find the first string value in the tree (depth-first)
    cJSON *found_string = NULL;
    // Simple iterative stack-based traversal using a fixed-size array to avoid recursion depth issues
    // We'll use a small stack of pointers (max depth 64) to keep it bounded
    cJSON *stack[64];
    int stack_size = 0;
    stack[stack_size++] = root;

    while (stack_size > 0 && found_string == NULL) {
        cJSON *current = stack[--stack_size];
        if (cJSON_IsString(current) && current->valuestring != NULL) {
            found_string = current;
            break;
        }
        // Push children in reverse order to simulate depth-first
        if (current->child != NULL) {
            // Collect children into a temporary array to reverse order
            cJSON *children[64];
            int child_count = 0;
            cJSON *child = current->child;
            while (child != NULL && child_count < 64) {
                children[child_count++] = child;
                child = child->next;
            }
            // Push in reverse so first child is processed first
            for (int i = child_count - 1; i >= 0; i--) {
                if (stack_size < 64) {
                    stack[stack_size++] = children[i];
                }
            }
        }
    }

    // Use the results to avoid optimization
    volatile int result = count;
    if (found_string != NULL) {
        result += (int)strlen(found_string->valuestring);
    }

    cJSON_Delete(root);
    return 0;
}