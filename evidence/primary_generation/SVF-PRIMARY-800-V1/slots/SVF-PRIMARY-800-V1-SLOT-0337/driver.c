#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include "cJSON.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size == 0) {
        return 0;
    }

    char *json_str = (char *)malloc(size + 1);
    if (json_str == NULL) {
        return 0;
    }
    memcpy(json_str, data, size);
    json_str[size] = '\0';

    cJSON *root = cJSON_Parse(json_str);
    free(json_str);
    if (root == NULL) {
        return 0;
    }

    cJSON *item = NULL;
    cJSON_ArrayForEach(item, root) {
        // Iterate over all items in the root object or array.
        // Accessing item is enough to exercise the iteration.
        volatile int dummy = (item->type != 0) ? 1 : 0;
        (void)dummy;
    }

    cJSON_Delete(root);
    return 0;
}