#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include "zlib.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 8) return 0;

    // Extract compression parameters from the first bytes
    int level = data[0] % 10;          // 0..9
    int method = data[1] % 8;          // Z_DEFLATED is 8, but allow others
    int windowBits = (data[2] % 16) + 8; // 8..23
    int memLevel = (data[3] % 9) + 1;  // 1..9
    int strategy = data[4] % 5;        // 0..4 (Z_FILTERED, Z_HUFFMAN_ONLY, Z_RLE, Z_FIXED, Z_DEFAULT_STRATEGY)

    // Use the rest of the data as input
    const uint8_t *input = data + 8;
    size_t input_size = size - 8;

    // Prepare output buffer (use a generous size)
    uLongf output_size = compressBound(input_size) + 1024;
    uint8_t *output = (uint8_t *)malloc(output_size);
    if (!output) return 0;

    z_stream stream;
    memset(&stream, 0, sizeof(stream));

    // Initialize deflate
    int ret = deflateInit2(&stream, level, method, windowBits, memLevel, strategy);
    if (ret != Z_OK) {
        free(output);
        return 0;
    }

    // Set input
    stream.next_in = (Bytef *)input;
    stream.avail_in = (uInt)input_size;

    // Set output
    stream.next_out = output;
    stream.avail_out = (uInt)output_size;

    // Compress in a single call (streaming interface)
    ret = deflate(&stream, Z_FINISH);
    if (ret != Z_STREAM_END && ret != Z_OK) {
        deflateEnd(&stream);
        free(output);
        return 0;
    }

    // Clean up
    deflateEnd(&stream);
    free(output);
    return 0;
}