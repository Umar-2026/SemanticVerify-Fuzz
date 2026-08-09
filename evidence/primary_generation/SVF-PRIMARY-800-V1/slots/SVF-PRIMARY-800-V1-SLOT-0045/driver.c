#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <stdlib.h>
#include "zlib.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 4) return 0;

    // Split input into two compressed payloads
    size_t split = (size_t)data[0] | ((size_t)data[1] << 8) | ((size_t)data[2] << 16) | ((size_t)data[3] << 24);
    split = split % (size - 3); // ensure at least 3 bytes for second payload
    split += 3; // offset past the split bytes

    const uint8_t *payload1 = data + 4;
    size_t payload1_size = split - 4;
    const uint8_t *payload2 = data + split;
    size_t payload2_size = size - split;

    if (payload1_size == 0 || payload2_size == 0) return 0;

    z_stream strm;
    memset(&strm, 0, sizeof(strm));

    // Initialize inflate
    if (inflateInit(&strm) != Z_OK) return 0;

    // Output buffer
    unsigned char out[4096];
    int ret;

    // Process first payload
    strm.next_in = (Bytef *)payload1;
    strm.avail_in = (uInt)payload1_size;
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
    strm.avail_in = (uInt)payload2_size;
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