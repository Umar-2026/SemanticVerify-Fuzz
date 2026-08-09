#include <stdlib.h>
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

    // First transformation: count the number of items in the tree
    int count = 0;
    cJSON *item = root;
    while (item != NULL) {
        count++;
        item = item->next;
    }

    // Second transformation: find the first string value in the tree (depth-first)
    cJSON *found = NULL;
    // Simple iterative traversal using a stack (bounded by tree size)
    // We'll use a fixed-size array stack; if tree is too deep, we skip.
    cJSON *stack[1024];
    int stack_size = 0;
    stack[stack_size++] = root;

    while (stack_size > 0 && found == NULL) {
        cJSON *current = stack[--stack_size];
        if (cJSON_IsString(current) && current->valuestring != NULL) {
            found = current;
            break;
        }
        // Push children in reverse order to simulate depth-first
        if (current->child != NULL) {
            // Collect children
            cJSON *child = current->child;
            int child_count = 0;
            while (child != NULL) {
                child_count++;
                child = child->next;
            }
            // Push in reverse
            child = current->child;
            // We'll push all children, but limit stack size
            if (stack_size + child_count <= 1024) {
                // Push in reverse order
                cJSON *children[1024];
                int idx = 0;
                while (child != NULL) {
                    children[idx++] = child;
                    child = child->next;
                }
                for (int i = idx - 1; i >= 0; i--) {
                    stack[stack_size++] = children[i];
                }
            }
        }
    }

    // Use the results to avoid optimization
    volatile int dummy = count;
    if (found != NULL) {
        dummy += (int)strlen(found->valuestring);
    }

    cJSON_Delete(root);
    return 0;
}