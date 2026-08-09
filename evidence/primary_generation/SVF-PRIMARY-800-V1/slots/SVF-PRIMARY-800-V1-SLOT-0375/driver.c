#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include "cJSON.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1) {
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

    cJSON_AddItemToObject(root, "items", array);

    size_t offset = 0;
    while (offset < size) {
        uint8_t type = data[offset] % 3;
        offset++;

        cJSON *child = NULL;
        switch (type) {
            case 0: {
                if (offset + 1 <= size) {
                    char buf[2] = {0};
                    buf[0] = (char)(data[offset] % 26 + 'a');
                    offset++;
                    child = cJSON_CreateString(buf);
                }
                break;
            }
            case 1: {
                if (offset + 4 <= size) {
                    int32_t val;
                    memcpy(&val, data + offset, 4);
                    offset += 4;
                    child = cJSON_CreateNumber((double)val);
                }
                break;
            }
            case 2: {
                if (offset + 1 <= size) {
                    child = cJSON_CreateBool(data[offset] % 2);
                    offset++;
                }
                break;
            }
            default:
                break;
        }

        if (child != NULL) {
            cJSON_AddItemToArray(array, child);
        } else {
            break;
        }
    }

    cJSON_Delete(root);
    return 0;
}