#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <stdlib.h>
#include "zlib.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

    int windowBits;
    uint8_t mode = data[0] % 3;
    switch (mode) {
        case 0:
            windowBits = 15;        /* zlib */
            break;
        case 1:
            windowBits = 15 + 16;   /* gzip */
            break;
        default:
            windowBits = -15;       /* raw */
            break;
    }

    z_stream strm;
    memset(&strm, 0, sizeof(strm));
    if (inflateInit2(&strm, windowBits) != Z_OK) {
        return 0;
    }

    /* Skip the mode byte, use the rest as compressed input */
    const uint8_t *input = data + 1;
    size_t input_size = size - 1;

    /* Allocate output buffer */
    size_t out_cap = 4096;
    uint8_t *out = (uint8_t *)malloc(out_cap);
    if (!out) {
        inflateEnd(&strm);
        return 0;
    }

    strm.next_in = (Bytef *)input;
    strm.avail_in = (uInt)input_size;
    if (strm.avail_in != input_size) {
        /* input too large for uInt, truncate */
        strm.avail_in = (uInt)-1;
    }

    int ret;
    do {
        strm.next_out = out;
        strm.avail_out = (uInt)out_cap;
        if (strm.avail_out != out_cap) {
            /* out_cap too large for uInt, cap */
            strm.avail_out = (uInt)-1;
        }
        ret = inflate(&strm, Z_NO_FLUSH);
        if (ret == Z_STREAM_ERROR || ret == Z_NEED_DICT || ret == Z_DATA_ERROR || ret == Z_MEM_ERROR) {
            break;
        }
        /* If output buffer filled and more input remains, continue */
        if (strm.avail_out == 0 && strm.avail_in > 0) {
            continue;
        }
    } while (ret == Z_OK && strm.avail_in > 0);

    inflateEnd(&strm);
    free(out);
    return 0;
}