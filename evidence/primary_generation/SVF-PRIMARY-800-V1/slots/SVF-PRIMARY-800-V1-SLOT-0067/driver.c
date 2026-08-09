#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <stdlib.h>
#include "zlib.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

    size_t half = size / 2;
    const uint8_t *part1 = data;
    size_t size1 = half;
    const uint8_t *part2 = data + half;
    size_t size2 = size - half;

    z_stream strm1;
    z_stream strm2;

    memset(&strm1, 0, sizeof(strm1));
    memset(&strm2, 0, sizeof(strm2));

    if (inflateInit(&strm1) != Z_OK) return 0;
    if (inflateInit(&strm2) != Z_OK) {
        inflateEnd(&strm1);
        return 0;
    }

    unsigned char out1[4096];
    unsigned char out2[4096];

    strm1.next_in = (Bytef *)part1;
    strm1.avail_in = (uInt)size1;
    strm1.next_out = out1;
    strm1.avail_out = sizeof(out1);

    strm2.next_in = (Bytef *)part2;
    strm2.avail_in = (uInt)size2;
    strm2.next_out = out2;
    strm2.avail_out = sizeof(out2);

    int ret1 = inflate(&strm1, Z_FINISH);
    int ret2 = inflate(&strm2, Z_FINISH);

    (void)ret1;
    (void)ret2;

    inflateEnd(&strm1);
    inflateEnd(&strm2);

    return 0;
}