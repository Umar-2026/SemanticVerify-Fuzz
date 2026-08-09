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

    // Iterate over all items in the root if it's an array or object
    cJSON *item = NULL;
    cJSON_ArrayForEach(item, root) {
        // Access item fields to ensure traversal
        if (item->type == cJSON_String) {
            // Just touch the value
            if (item->valuestring != NULL) {
                // no-op
            }
        } else if (item->type == cJSON_Number) {
            // no-op
        } else if (item->type == cJSON_Array || item->type == cJSON_Object) {
            // Recursively iterate nested containers
            cJSON *nested = NULL;
            cJSON_ArrayForEach(nested, item) {
                // Touch nested items
                if (nested->type == cJSON_String) {
                    if (nested->valuestring != NULL) {
                        // no-op
                    }
                }
            }
        }
    }

    cJSON_Delete(root);
    return 0;
}