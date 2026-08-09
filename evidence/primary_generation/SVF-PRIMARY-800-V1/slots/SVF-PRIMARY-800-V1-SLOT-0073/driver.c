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

    // Feed first branch
    strm.next_in = (Bytef *)branch1;
    strm.avail_in = (uInt)branch1_size;
    unsigned char out1[4096];
    strm.next_out = out1;
    strm.avail_out = sizeof(out1);
    int ret = inflate(&strm, Z_NO_FLUSH);
    if (ret != Z_OK && ret != Z_STREAM_END && ret != Z_BUF_ERROR) {
        inflateEnd(&strm);
        return 0;
    }

    // Copy the state
    z_stream copy;
    memset(&copy, 0, sizeof(copy));
    if (inflateCopy(&copy, &strm) != Z_OK) {
        inflateEnd(&strm);
        return 0;
    }

    // Continue with second branch on the copy
    copy.next_in = (Bytef *)branch2;
    copy.avail_in = (uInt)branch2_size;
    unsigned char out2[4096];
    copy.next_out = out2;
    copy.avail_out = sizeof(out2);
    ret = inflate(&copy, Z_FINISH);
    if (ret != Z_OK && ret != Z_STREAM_END && ret != Z_BUF_ERROR) {
        // ignore errors
    }

    // Clean up
    inflateEnd(&copy);
    inflateEnd(&strm);
    return 0;
}