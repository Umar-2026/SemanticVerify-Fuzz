#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include "zlib.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) {
        return 0;
    }

    size_t split_point = data[0] % size;
    const uint8_t *part1 = data + 1;
    size_t size1 = split_point;
    const uint8_t *part2 = data + 1 + split_point;
    size_t size2 = size - 1 - split_point;

    z_stream strm1, strm2;
    memset(&strm1, 0, sizeof(strm1));
    memset(&strm2, 0, sizeof(strm2));

    if (inflateInit(&strm1) != Z_OK || inflateInit(&strm2) != Z_OK) {
        return 0;
    }

    uint8_t buffer[1024];

    strm1.next_in = (Bytef *)part1;
    strm1.avail_in = (uInt)size1;
    strm1.next_out = buffer;
    strm1.avail_out = sizeof(buffer);
    inflate(&strm1, Z_NO_FLUSH);

    strm2.next_in = (Bytef *)part2;
    strm2.avail_in = (uInt)size2;
    strm2.next_out = buffer;
    strm2.avail_out = sizeof(buffer);
    inflate(&strm2, Z_NO_FLUSH);

    inflateEnd(&strm1);
    inflateEnd(&strm2);

    return 0;
}