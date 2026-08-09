#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <stdlib.h>
#include "zlib.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

    // Split input: first byte determines dictionary size fraction, second byte determines compression level
    size_t dict_size = (size_t)(data[0]) * (size - 2) / 255;
    if (dict_size > size - 2) dict_size = size - 2;
    int level = (data[1] % 10); // 0-9

    const uint8_t *dict = data + 2;
    size_t dict_len = dict_size;
    const uint8_t *src = data + 2 + dict_len;
    size_t src_len = size - 2 - dict_len;

    if (src_len == 0) return 0;

    // Prepare output buffer with some slack
    uLongf dest_len = compressBound(src_len) + 1024;
    Bytef *dest = (Bytef *)malloc(dest_len);
    if (!dest) return 0;

    z_stream strm;
    memset(&strm, 0, sizeof(strm));

    if (deflateInit(&strm, level) != Z_OK) {
        free(dest);
        return 0;
    }

    // Set dictionary if we have one
    if (dict_len > 0) {
        if (deflateSetDictionary(&strm, dict, (uInt)dict_len) != Z_OK) {
            deflateEnd(&strm);
            free(dest);
            return 0;
        }
    }

    strm.next_in = (Bytef *)src;
    strm.avail_in = (uInt)src_len;
    strm.next_out = dest;
    strm.avail_out = (uInt)dest_len;

    int ret = deflate(&strm, Z_FINISH);
    if (ret != Z_STREAM_END && ret != Z_OK) {
        // Not a failure per se, just incomplete; ignore
    }

    deflateEnd(&strm);
    free(dest);
    return 0;
}