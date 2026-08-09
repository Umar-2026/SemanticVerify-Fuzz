#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include "zlib.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

    int windowBits;
    uint8_t mode = data[0] % 3;
    switch (mode) {
        case 0:
            windowBits = 15; /* zlib */
            break;
        case 1:
            windowBits = 15 + 32; /* gzip */
            break;
        default:
            windowBits = -15; /* raw */
            break;
    }

    z_stream strm;
    memset(&strm, 0, sizeof(strm));
    if (inflateInit2(&strm, windowBits) != Z_OK) {
        return 0;
    }

    /* Skip the first byte used for mode selection */
    const uint8_t *comp_data = data + 1;
    size_t comp_size = size - 1;

    strm.next_in = (Bytef *)comp_data;
    strm.avail_in = (uInt)comp_size;

    /* Output buffer */
    uint8_t out[4096];
    int ret;

    do {
        strm.next_out = out;
        strm.avail_out = sizeof(out);
        ret = inflate(&strm, Z_NO_FLUSH);
        if (ret != Z_OK && ret != Z_STREAM_END && ret != Z_BUF_ERROR) {
            break;
        }
    } while (ret != Z_STREAM_END && strm.avail_in > 0);

    inflateEnd(&strm);
    return 0;
}