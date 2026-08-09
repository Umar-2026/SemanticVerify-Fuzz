#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <stdlib.h>
#include "zlib.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

    // Split input into two branches
    size_t split = data[0] % (size - 1) + 1;
    const uint8_t *branch1 = data + 1;
    size_t branch1_size = split - 1;
    const uint8_t *branch2 = data + split;
    size_t branch2_size = size - split;

    // Initialize decompression state
    z_stream strm;
    memset(&strm, 0, sizeof(strm));
    if (inflateInit(&strm) != Z_OK) return 0;

    // Process first branch
    strm.next_in = (Bytef *)branch1;
    strm.avail_in = (uInt)branch1_size;
    unsigned char out1[1024];
    int ret;
    do {
        strm.next_out = out1;
        strm.avail_out = sizeof(out1);
        ret = inflate(&strm, Z_NO_FLUSH);
        if (ret != Z_OK && ret != Z_STREAM_END && ret != Z_BUF_ERROR) {
            inflateEnd(&strm);
            return 0;
        }
    } while (ret != Z_STREAM_END && strm.avail_in > 0 && ret != Z_BUF_ERROR);

    // Copy the state
    z_stream copy;
    memset(&copy, 0, sizeof(copy));
    if (inflateCopy(&copy, &strm) != Z_OK) {
        inflateEnd(&strm);
        return 0;
    }

    // Continue processing second branch using the copy
    copy.next_in = (Bytef *)branch2;
    copy.avail_in = (uInt)branch2_size;
    unsigned char out2[1024];
    do {
        copy.next_out = out2;
        copy.avail_out = sizeof(out2);
        ret = inflate(&copy, Z_NO_FLUSH);
        if (ret != Z_OK && ret != Z_STREAM_END && ret != Z_BUF_ERROR) {
            inflateEnd(&strm);
            inflateEnd(&copy);
            return 0;
        }
    } while (ret != Z_STREAM_END && copy.avail_in > 0 && ret != Z_BUF_ERROR);

    // Clean up
    inflateEnd(&strm);
    inflateEnd(&copy);
    return 0;
}