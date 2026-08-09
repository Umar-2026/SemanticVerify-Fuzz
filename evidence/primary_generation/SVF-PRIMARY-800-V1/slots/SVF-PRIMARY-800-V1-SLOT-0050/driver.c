#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include "zlib.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 4) {
        return 0;
    }

    size_t half = size / 2;
    const uint8_t *data1 = data;
    size_t size1 = half;
    const uint8_t *data2 = data + half;
    size_t size2 = size - half;

    z_stream strm;
    memset(&strm, 0, sizeof(strm));

    if (inflateInit(&strm) != Z_OK) {
        return 0;
    }

    uint8_t out[1024];

    strm.next_in = (Bytef *)data1;
    strm.avail_in = (uInt)size1;
    strm.next_out = out;
    strm.avail_out = sizeof(out);

    inflate(&strm, Z_FINISH);

    if (inflateReset(&strm) != Z_OK) {
        inflateEnd(&strm);
        return 0;
    }

    strm.next_in = (Bytef *)data2;
    strm.avail_in = (uInt)size2;
    strm.next_out = out;
    strm.avail_out = sizeof(out);

    inflate(&strm, Z_FINISH);

    inflateEnd(&strm);

    return 0;
}