#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include "zlib.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 5) {
        return 0;
    }

    z_stream strm;
    memset(&strm, 0, sizeof(strm));

    int level = (data[0] % 10) - 1;
    int method = Z_DEFLATED;
    int windowBits = (data[1] % 15) + 8;
    int memLevel = (data[2] % 9) + 1;
    int strategy = (data[3] % 4);

    if (deflateInit2(&strm, level, method, windowBits, memLevel, strategy) != Z_OK) {
        return 0;
    }

    size_t out_size = deflateBound(&strm, size);
    uint8_t *out_buf = malloc(out_size);
    if (!out_buf) {
        deflateEnd(&strm);
        return 0;
    }

    strm.next_in = (Bytef *)data + 4;
    strm.avail_in = (uInt)(size - 4);
    strm.next_out = out_buf;
    strm.avail_out = (uInt)out_size;

    deflate(&strm, Z_FINISH);
    deflateEnd(&strm);

    free(out_buf);
    return 0;
}