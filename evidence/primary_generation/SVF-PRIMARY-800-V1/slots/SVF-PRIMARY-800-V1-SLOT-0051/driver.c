#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include "zlib.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

    // Split input: first byte determines dictionary size fraction, rest is data.
    size_t dict_size = (size_t)data[0] * (size - 1) / 255;
    if (dict_size > size - 1) dict_size = size - 1;
    const uint8_t *dict = data + 1;
    const uint8_t *src = data + 1 + dict_size;
    size_t src_size = size - 1 - dict_size;

    if (src_size == 0) return 0;

    // Prepare output buffer with some slack.
    uLongf dest_capacity = compressBound((uLong)src_size) + 1024;
    uint8_t *dest = (uint8_t *)malloc(dest_capacity);
    if (!dest) return 0;

    z_stream strm;
    memset(&strm, 0, sizeof(strm));

    if (deflateInit(&strm, Z_DEFAULT_COMPRESSION) != Z_OK) {
        free(dest);
        return 0;
    }

    // Set dictionary if we have one.
    if (dict_size > 0) {
        if (deflateSetDictionary(&strm, dict, (uInt)dict_size) != Z_OK) {
            deflateEnd(&strm);
            free(dest);
            return 0;
        }
    }

    strm.next_in = (Bytef *)src;
    strm.avail_in = (uInt)src_size;
    strm.next_out = dest;
    strm.avail_out = (uInt)dest_capacity;

    int ret = deflate(&strm, Z_FINISH);
    if (ret != Z_STREAM_END && ret != Z_OK) {
        // Not a failure per se, just stop.
    }

    deflateEnd(&strm);
    free(dest);
    return 0;
}