#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <stdlib.h>
#include "zlib.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

    z_stream strm;
    memset(&strm, 0, sizeof(strm));

    if (inflateInit(&strm) != Z_OK) {
        return 0;
    }

    /* Use first byte to choose windowBits for inflateInit2? No, we use inflateInit as required. */
    /* Use second byte to control flush behavior */
    int flush = (data[1] & 1) ? Z_FINISH : Z_NO_FLUSH;

    /* Provide input in chunks to exercise streaming */
    size_t chunk_size = 1 + (data[0] % 16);
    if (chunk_size == 0) chunk_size = 1;

    strm.next_in = (Bytef *)data;
    strm.avail_in = (uInt)size;
    strm.next_out = (Bytef *)malloc(256);
    if (!strm.next_out) {
        inflateEnd(&strm);
        return 0;
    }

    int ret = Z_OK;
    size_t total_out = 0;
    size_t consumed = 0;

    while (consumed < size) {
        size_t in_chunk = size - consumed;
        if (in_chunk > chunk_size) in_chunk = chunk_size;

        strm.next_in = (Bytef *)(data + consumed);
        strm.avail_in = (uInt)in_chunk;
        strm.next_out = (Bytef *)malloc(256);
        if (!strm.next_out) {
            break;
        }
        strm.avail_out = 256;

        ret = inflate(&strm, flush);

        total_out += 256 - strm.avail_out;
        free(strm.next_out);
        strm.next_out = NULL;

        consumed += in_chunk - strm.avail_in;

        if (ret == Z_STREAM_END) {
            break;
        }
        if (ret != Z_OK && ret != Z_BUF_ERROR) {
            break;
        }
        if (flush == Z_FINISH && ret == Z_BUF_ERROR) {
            /* Not enough input for finish, continue */
        }
    }

    /* Different functional outcomes based on ret */
    if (ret == Z_STREAM_END) {
        /* Success: consume all input? Not necessarily, but we can check */
        if (strm.total_in == size) {
            /* All input consumed */
        }
    } else if (ret == Z_OK || ret == Z_BUF_ERROR) {
        /* Need more input or output space */
    } else if (ret == Z_DATA_ERROR) {
        /* Corrupt data */
    } else if (ret == Z_MEM_ERROR) {
        /* Memory error */
    } else if (ret == Z_NEED_DICT) {
        /* Dictionary required */
    } else {
        /* Other error */
    }

    inflateEnd(&strm);
    return 0;
}