#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <stdlib.h>
#include "zlib.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1) return 0;

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

    /* Skip the mode byte for the compressed data */
    const uint8_t *comp_data = data + 1;
    size_t comp_size = size - 1;

    /* Use a small output buffer to force multiple inflate calls */
    uint8_t outbuf[256];
    strm.next_in = (Bytef *)comp_data;
    strm.avail_in = (uInt)comp_size;
    strm.next_out = outbuf;
    strm.avail_out = sizeof(outbuf);

    int ret;
    do {
        ret = inflate(&strm, Z_NO_FLUSH);
        if (ret == Z_STREAM_END) {
            break;
        }
        if (ret != Z_OK && ret != Z_BUF_ERROR) {
            break;
        }
        if (strm.avail_out == 0) {
            strm.next_out = outbuf;
            strm.avail_out = sizeof(outbuf);
        }
        if (strm.avail_in == 0 && ret != Z_STREAM_END) {
            break;
        }
    } while (ret == Z_OK || ret == Z_BUF_ERROR);

    inflateEnd(&strm);
    return 0;
}