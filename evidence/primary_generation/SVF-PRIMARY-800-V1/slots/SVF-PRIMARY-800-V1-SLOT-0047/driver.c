#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <stdlib.h>
#include "zlib.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

    // Split input into two compressed payloads
    size_t split = (size_t)data[0] * 256 + data[1];
    if (split >= size) split = size / 2;
    if (split == 0) split = 1;

    const uint8_t *payload1 = data + 2;
    size_t payload1_size = split;
    if (payload1_size > size - 2) payload1_size = size - 2;

    const uint8_t *payload2 = data + 2 + payload1_size;
    size_t payload2_size = size - 2 - payload1_size;

    // Initialize z_stream
    z_stream strm;
    memset(&strm, 0, sizeof(strm));
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