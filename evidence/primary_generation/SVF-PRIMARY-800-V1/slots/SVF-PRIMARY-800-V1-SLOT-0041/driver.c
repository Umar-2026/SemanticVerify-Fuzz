#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <stdlib.h>
#include "zlib.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

    // Split input into two compressed payloads
    size_t split = (size_t)data[0] * 257 % (size - 1) + 1;
    const uint8_t *payload1 = data + 1;
    size_t len1 = split;
    const uint8_t *payload2 = data + 1 + split;
    size_t len2 = size - 1 - split;

    if (len1 == 0 || len2 == 0) return 0;

    z_stream strm;
    memset(&strm, 0, sizeof(strm));

    // Initialize inflate
    if (inflateInit(&strm) != Z_OK) return 0;

    // Output buffer
    unsigned char out[4096];
    int ret;

    // Process first payload
    strm.next_in = (Bytef *)payload1;
    strm.avail_in = (uInt)len1;
    do {
        strm.next_out = out;
        strm.avail_out = sizeof(out);
        ret = inflate(&strm, Z_NO_FLUSH);
        if (ret != Z_OK && ret != Z_STREAM_END && ret != Z_BUF_ERROR) {
            inflateEnd(&strm);
            return 0;
        }
    } while (ret != Z_STREAM_END && strm.avail_in > 0);

    // Reset stream for second payload
    if (inflateReset(&strm) != Z_OK) {
        inflateEnd(&strm);
        return 0;
    }

    // Process second payload
    strm.next_in = (Bytef *)payload2;
    strm.avail_in = (uInt)len2;
    do {
        strm.next_out = out;
        strm.avail_out = sizeof(out);
        ret = inflate(&strm, Z_NO_FLUSH);
        if (ret != Z_OK && ret != Z_STREAM_END && ret != Z_BUF_ERROR) {
            inflateEnd(&strm);
            return 0;
        }
    } while (ret != Z_STREAM_END && strm.avail_in > 0);

    inflateEnd(&strm);
    return 0;
}