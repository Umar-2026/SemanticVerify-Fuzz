#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <stdlib.h>
#include "zlib.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

    // Split input: first half for initial stream, second half for branch processing
    size_t half = size / 2;
    const uint8_t *init_data = data;
    size_t init_size = half;
    const uint8_t *branch_data = data + half;
    size_t branch_size = size - half;

    // Initialize decompression stream
    z_stream strm;
    memset(&strm, 0, sizeof(strm));
    if (inflateInit(&strm) != Z_OK) return 0;

    // Feed initial data
    strm.next_in = (Bytef *)init_data;
    strm.avail_in = (uInt)init_size;

    // Output buffer
    unsigned char out[256];
    int ret;

    // Process initial data until input consumed or error
    do {
        strm.next_out = out;
        strm.avail_out = sizeof(out);
        ret = inflate(&strm, Z_NO_FLUSH);
        if (ret == Z_STREAM_ERROR || ret == Z_NEED_DICT || ret == Z_DATA_ERROR || ret == Z_MEM_ERROR) {
            inflateEnd(&strm);
            return 0;
        }
    } while (strm.avail_in > 0 && ret != Z_STREAM_END);

    // Copy the stream state
    z_stream copy;
    memset(&copy, 0, sizeof(copy));
    if (inflateCopy(&copy, &strm) != Z_OK) {
        inflateEnd(&strm);
        return 0;
    }

    // Process branch data with the copy
    copy.next_in = (Bytef *)branch_data;
    copy.avail_in = (uInt)branch_size;

    do {
        copy.next_out = out;
        copy.avail_out = sizeof(out);
        ret = inflate(&copy, Z_NO_FLUSH);
        if (ret == Z_STREAM_ERROR || ret == Z_NEED_DICT || ret == Z_DATA_ERROR || ret == Z_MEM_ERROR) {
            break;
        }
    } while (copy.avail_in > 0 && ret != Z_STREAM_END);

    // Cleanup
    inflateEnd(&copy);
    inflateEnd(&strm);
    return 0;
}