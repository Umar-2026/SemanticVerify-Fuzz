#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <stdlib.h>
#include "zlib.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

    // Split input: first byte determines dictionary size, second byte determines compression level
    size_t dict_size = data[0];
    int level = data[1] % 10; // 0-9

    // Remaining data: first part is dictionary, second part is input to compress
    if (size < 2 + dict_size) return 0;
    const uint8_t *dict = data + 2;
    const uint8_t *input = data + 2 + dict_size;
    size_t input_size = size - 2 - dict_size;
    if (input_size == 0) return 0;

    // Prepare output buffer
    uLongf compressed_size = compressBound(input_size);
    uint8_t *compressed = (uint8_t *)malloc(compressed_size);
    if (!compressed) return 0;

    z_stream strm;
    memset(&strm, 0, sizeof(strm));

    // Initialize deflate
    if (deflateInit(&strm, level) != Z_OK) {
        free(compressed);
        return 0;
    }

    // Set dictionary if dict_size > 0
    if (dict_size > 0) {
        if (deflateSetDictionary(&strm, dict, dict_size) != Z_OK) {
            deflateEnd(&strm);
            free(compressed);
            return 0;
        }
    }

    // Set input and output
    strm.next_in = (Bytef *)input;
    strm.avail_in = (uInt)input_size;
    strm.next_out = compressed;
    strm.avail_out = (uInt)compressed_size;

    // Compress in streaming fashion (may need multiple calls, but we do one call with Z_FINISH)
    int ret = deflate(&strm, Z_FINISH);
    if (ret != Z_STREAM_END && ret != Z_OK) {
        deflateEnd(&strm);
        free(compressed);
        return 0;
    }

    // Clean up
    deflateEnd(&strm);
    free(compressed);
    return 0;
}