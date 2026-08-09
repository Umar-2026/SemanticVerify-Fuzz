#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <stdlib.h>
#include "zlib.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) {
        return 0;
    }

    z_stream strm;
    memset(&strm, 0, sizeof(strm));

    int windowBits;
    uint8_t mode = data[0] & 0x03;
    switch (mode) {
        case 0:
            windowBits = 15;        /* zlib */
            break;
        case 1:
            windowBits = 15 + 16;   /* gzip */
            break;
        case 2:
            windowBits = -15;       /* raw */
            break;
        default:
            windowBits = 15;        /* default to zlib */
            break;
    }

    if (inflateInit2(&strm, windowBits) != Z_OK) {
        return 0;
    }

    /* Use the second byte to decide chunk size for streaming */
    size_t chunk_size = (size_t)(data[1] % 64) + 1;
    if (chunk_size > size - 2) {
        chunk_size = size - 2;
    }
    if (chunk_size == 0) {
        chunk_size = 1;
    }

    const uint8_t *input = data + 2;
    size_t input_size = size - 2;

    uint8_t output[256];
    int ret = Z_OK;

    size_t offset = 0;
    while (offset < input_size) {
        size_t to_consume = chunk_size;
        if (to_consume > input_size - offset) {
            to_consume = input_size - offset;
        }

        strm.next_in = (Bytef *)(input + offset);
        strm.avail_in = (uInt)to_consume;
        offset += to_consume;

        do {
            strm.next_out = output;
            strm.avail_out = sizeof(output);
            ret = inflate(&strm, Z_NO_FLUSH);
            if (ret != Z_OK && ret != Z_STREAM_END && ret != Z_BUF_ERROR) {
                break;
            }
        } while (strm.avail_out == 0 && ret != Z_STREAM_END);

        if (ret != Z_OK && ret != Z_STREAM_END && ret != Z_BUF_ERROR) {
            break;
        }
        if (ret == Z_STREAM_END) {
            break;
        }
    }

    inflateEnd(&strm);
    return 0;
}