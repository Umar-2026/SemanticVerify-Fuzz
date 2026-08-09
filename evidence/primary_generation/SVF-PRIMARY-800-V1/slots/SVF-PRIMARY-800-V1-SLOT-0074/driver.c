#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <zlib.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 16) {
        return 0;
    }

    z_stream strm1, strm2;
    memset(&strm1, 0, sizeof(z_stream));
    memset(&strm2, 0, sizeof(z_stream));

    if (inflateInit(&strm1) != Z_OK) {
        return 0;
    }

    strm1.next_in = (Bytef *)data;
    strm1.avail_in = (uInt)(size / 2);

    unsigned char out1[1024];
    strm1.next_out = out1;
    strm1.avail_out = sizeof(out1);

    inflate(&strm1, Z_NO_FLUSH);

    if (inflateCopy(&strm2, &strm1) == Z_OK) {
        strm2.next_in = (Bytef *)(data + (size / 2));
        strm2.avail_in = (uInt)(size - (size / 2));

        unsigned char out2[1024];
        strm2.next_out = out2;
        strm2.avail_out = sizeof(out2);

        inflate(&strm2, Z_FINISH);
        inflateEnd(&strm2);
    }

    inflateEnd(&strm1);

    return 0;
}