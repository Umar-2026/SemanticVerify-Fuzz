#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <stdlib.h>
#include "zlib.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

    // Split input into two halves
    size_t split = size / 2;
    const uint8_t *data1 = data;
    size_t size1 = split;
    const uint8_t *data2 = data + split;
    size_t size2 = size - split;

    // Initialize two independent z_stream objects
    z_stream strm1, strm2;
    memset(&strm1, 0, sizeof(strm1));
    memset(&strm2, 0, sizeof(strm2));

    // Initialize inflate for both streams
    if (inflateInit(&strm1) != Z_OK) return 0;
    if (inflateInit(&strm2) != Z_OK) {
        inflateEnd(&strm1);
        return 0;
    }

    // Output buffers
    unsigned char out1[4096];
    unsigned char out2[4096];

    // Process first part
    strm1.next_in = (Bytef *)data1;
    strm1.avail_in = (uInt)size1;
    strm1.next_out = out1;
    strm1.avail_out = sizeof(out1);

    int ret1 = inflate(&strm1, Z_FINISH);
    if (ret1 != Z_STREAM_END && ret1 != Z_OK && ret1 != Z_BUF_ERROR) {
        inflateEnd(&strm1);
        inflateEnd(&strm2);
        return 0;
    }

    // Process second part
    strm2.next_in = (Bytef *)data2;
    strm2.avail_in = (uInt)size2;
    strm2.next_out = out2;
    strm2.avail_out = sizeof(out2);

    int ret2 = inflate(&strm2, Z_FINISH);
    if (ret2 != Z_STREAM_END && ret2 != Z_OK && ret2 != Z_BUF_ERROR) {
        inflateEnd(&strm1);
        inflateEnd(&strm2);
        return 0;
    }

    // Clean up
    inflateEnd(&strm1);
    inflateEnd(&strm2);

    return 0;
}