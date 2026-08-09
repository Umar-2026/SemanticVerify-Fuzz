#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <stdlib.h>
#include "zlib.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

    int windowBits;
    uint8_t mode = data[0] & 0x03;
    switch (mode) {
        case 0:
            windowBits = 15; /* zlib */
            break;
        case 1:
            windowBits = 15 + 16; /* gzip */
            break;
        case 2:
            windowBits = -15; /* raw */
            break;
        default:
            windowBits = 15; /* fallback */
            break;
    }

    /* Use the second byte to influence flush behavior */
    int flush = (data[1] & 0x01) ? Z_FINISH : Z_NO_FLUSH;

    z_stream strm;
    memset(&strm, 0, sizeof(strm));

    if (inflateInit2(&strm, windowBits) != Z_OK) {
        return 0;
    }

    /* Skip the first two bytes used for mode selection */
    const uint8_t *input = data + 2;
    size_t input_size = size - 2;

    /* Limit input size to avoid excessive memory usage */
    if (input_size > 1024 * 1024) {
        input_size = 1024 * 1024;
    }

    strm.next_in = (Bytef *)input;
    strm.avail_in = (uInt)input_size;

    /* Output buffer */
    unsigned char out[4096];
    int ret;

    do {
        strm.next_out = out;
        strm.avail_out = sizeof(out);

        ret = inflate(&strm, flush);

        if (ret != Z_OK && ret != Z_STREAM_END && ret != Z_BUF_ERROR) {
            break;
        }

        /* If we've consumed all input and still need more, stop */
        if (strm.avail_in == 0 && ret != Z_STREAM_END) {
            break;
        }

    } while (ret != Z_STREAM_END && strm.avail_out == 0);

    inflateEnd(&strm);
    return 0;
}