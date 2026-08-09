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

    // First transformation: count all items in the tree (recursive)
    int count = 0;
    cJSON *item = root;
    // Simple iterative traversal using cJSON_GetArraySize and cJSON_GetArrayItem
    // For objects and arrays, traverse children; for primitives, just count.
    // Use a stack to avoid recursion depth issues.
    cJSON **stack = (cJSON **)malloc(sizeof(cJSON *) * 1024);
    if (!stack) {
        cJSON_Delete(root);
        return 0;
    }
    int stack_size = 1024;
    int top = 0;
    stack[top++] = root;
    while (top > 0) {
        cJSON *current = stack[--top];
        count++;
        if (cJSON_IsArray(current) || cJSON_IsObject(current)) {
            int array_size = cJSON_GetArraySize(current);
            for (int i = 0; i < array_size; i++) {
                cJSON *child = cJSON_GetArrayItem(current, i);
                if (child) {
                    if (top >= stack_size) {
                        stack_size *= 2;
                        cJSON **new_stack = (cJSON **)realloc(stack, sizeof(cJSON *) * stack_size);
                        if (!new_stack) {
                            free(stack);
                            cJSON_Delete(root);
                            return 0;
                        }
                        stack = new_stack;
                    }
                    stack[top++] = child;
                }
            }
        }
    }
    free(stack);

    // Second transformation: find the maximum depth of the tree
    int max_depth = 0;
    // Use a simple recursive function via a helper (bounded by input size)
    // We'll implement an iterative depth-first search with depth tracking.
    typedef struct {
        cJSON *node;
        int depth;
    } StackEntry;
    StackEntry *depth_stack = (StackEntry *)malloc(sizeof(StackEntry) * 1024);
    if (!depth_stack) {
        cJSON_Delete(root);
        return 0;
    }
    int depth_stack_size = 1024;
    int depth_top = 0;
    depth_stack[depth_top].node = root;
    depth_stack[depth_top].depth = 1;
    depth_top++;
    while (depth_top > 0) {
        StackEntry entry = depth_stack[--depth_top];
        if (entry.depth > max_depth) {
            max_depth = entry.depth;
        }
        if (cJSON_IsArray(entry.node) || cJSON_IsObject(entry.node)) {
            int array_size = cJSON_GetArraySize(entry.node);
            for (int i = 0; i < array_size; i++) {
                cJSON *child = cJSON_GetArrayItem(entry.node, i);
                if (child) {
                    if (depth_top >= depth_stack_size) {
                        depth_stack_size *= 2;
                        StackEntry *new_stack = (StackEntry *)realloc(depth_stack, sizeof(StackEntry) * depth_stack_size);
                        if (!new_stack) {
                            free(depth_stack);
                            cJSON_Delete(root);
                            return 0;
                        }
                        depth_stack = new_stack;
                    }
                    depth_stack[depth_top].node = child;
                    depth_stack[depth_top].depth = entry.depth + 1;
                    depth_top++;
                }
            }
        }
    }
    free(depth_stack);

    // Use the results to avoid optimization (e.g., sum them and compare)
    volatile int result = count + max_depth;
    (void)result;

    cJSON_Delete(root);
    return 0;
}