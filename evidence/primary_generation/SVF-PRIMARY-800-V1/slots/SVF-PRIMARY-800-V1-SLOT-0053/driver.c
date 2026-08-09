#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <stdlib.h>
#include "zlib.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

    // Split input: first byte determines dictionary size fraction, rest is data.
    // We'll use a simple scheme: dictionary size = data[0] % (size/2 + 1), capped.
    size_t dict_size = data[0];
    if (size > 1) {
        dict_size = dict_size % (size - 1);
    } else {
        dict_size = 0;
    }
    // Ensure dictionary size doesn't exceed available data after the first byte.
    if (dict_size > size - 1) dict_size = size - 1;

    const uint8_t *dict = data + 1;
    const uint8_t *src = data + 1 + dict_size;
    size_t src_size = size - 1 - dict_size;

    if (src_size == 0) return 0;

    // Prepare output buffer: worst-case zlib deflate bound.
    uLongf bound = compressBound((uLong)src_size);
    if (bound == 0) return 0;
    Bytef *out = (Bytef *)malloc(bound);
    if (!out) return 0;

    z_stream strm;
    memset(&strm, 0, sizeof(strm));

    int ret = deflateInit(&strm, Z_DEFAULT_COMPRESSION);
    if (ret != Z_OK) {
        free(out);
        return 0;
    }

    // Set dictionary if we have one.
    if (dict_size > 0) {
        ret = deflateSetDictionary(&strm, dict, (uInt)dict_size);
        if (ret != Z_OK) {
            deflateEnd(&strm);
            free(out);
            return 0;
        }
    }

    strm.next_in = (Bytef *)src;
    strm.avail_in = (uInt)src_size;
    strm.next_out = out;
    strm.avail_out = (uInt)bound;

    // Stream compression: feed all input, then finish.
    ret = deflate(&strm, Z_FINISH);
    if (ret != Z_STREAM_END) {
        // Could be Z_BUF_ERROR if output too small, but bound should be enough.
        deflateEnd(&strm);
        free(out);
        return 0;
    }

    // Consume compressed output (just to ensure it's used).
    size_t compressed_size = bound - strm.avail_out;
    (void)compressed_size;

    deflateEnd(&strm);
    free(out);
    return 0;
}