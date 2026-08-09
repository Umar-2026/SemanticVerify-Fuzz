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
    unsigned char out1[256];
    int ret1 = Z_OK;
    while (strm.avail_in > 0 && ret1 == Z_OK) {
        strm.next_out = out1;
        strm.avail_out = sizeof(out1);
        ret1 = inflate(&strm, Z_NO_FLUSH);
    }

    // Copy state
    z_stream copy;
    memset(&copy, 0, sizeof(copy));
    if (inflateCopy(&copy, &strm) != Z_OK) {
        inflateEnd(&strm);
        return 0;
    }

    // Continue with second branch on the copy
    copy.next_in = (Bytef *)branch2;
    copy.avail_in = (uInt)branch2_size;
    unsigned char out2[256];
    int ret2 = Z_OK;
    while (copy.avail_in > 0 && ret2 == Z_OK) {
        copy.next_out = out2;
        copy.avail_out = sizeof(out2);
        ret2 = inflate(&copy, Z_NO_FLUSH);
    }

    // Cleanup
    inflateEnd(&strm);
    inflateEnd(&copy);
    return 0;
}