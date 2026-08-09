#include <stdint.h>
#include <stdlib.h>
#include "cJSON.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 4) {
        return 0;
    }

    cJSON *root = cJSON_CreateObject();
    if (root == NULL) {
        return 0;
    }

    cJSON *array = cJSON_CreateArray();
    if (array == NULL) {
        cJSON_Delete(root);
        return 0;
    }

    cJSON_AddItemToObject(root, "fuzz_array", array);

    for (size_t i = 0; i + 2 < size; i += 3) {
        cJSON *item;
        uint8_t type = data[i] % 3;

        if (type == 0) {
            item = cJSON_CreateNumber((double)data[i + 1]);
        } else if (type == 1) {
            item = cJSON_CreateString("fuzz_str");
        } else {
            item = cJSON_CreateObject();
            cJSON_AddItemToObject(item, "nested_key", cJSON_CreateNumber((double)data[i + 2]));
        }

        if (item != NULL) {
            cJSON_AddItemToArray(array, item);
        }
    }

    char *out = cJSON_Print(root);
    if (out != NULL) {
        free(out);
    }

    cJSON_Delete(root);
    return 0;
}