#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <stdlib.h>
#include "zlib.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 8) {
        return 0;
    }

    // Extract compression parameters from the first 8 bytes
    int level = data[0] % 10;          // 0..9
    int method = data[1] % 8;          // Z_DEFLATED is 8, but allow some invalid values
    int windowBits = (int)(data[2] % 16) - 8; // -8..7, but zlib expects 8..15 or -8..-15
    // Adjust windowBits to valid range: 8..15 or -8..-15
    if (windowBits >= 0) {
        windowBits = 8 + (windowBits % 8); // 8..15
    } else {
        windowBits = -8 - ((-windowBits) % 8); // -8..-15
    }
    int memLevel = 1 + (data[3] % 9);  // 1..9
    int strategy = data[4] % 5;        // 0..4 (Z_FILTERED, Z_HUFFMAN_ONLY, Z_RLE, Z_FIXED, Z_DEFAULT_STRATEGY)

    // Use remaining bytes as input
    const uint8_t *input = data + 8;
    size_t input_size = size - 8;

    // Prepare output buffer: worst case is input_size + input_size/1000 + 13
    uLongf output_capacity = (uLongf)input_size + (input_size / 1000) + 13;
    if (output_capacity < 1024) {
        output_capacity = 1024;
    }
    Bytef *output = (Bytef *)malloc(output_capacity);
    if (output == NULL) {
        return 0;
    }

    z_stream strm;
    memset(&strm, 0, sizeof(strm));

    // Initialize deflate stream
    int ret = deflateInit2(&strm, level, method, windowBits, memLevel, strategy);
    if (ret != Z_OK) {
        free(output);
        return 0;
    }

    strm.next_in = (Bytef *)input;
    strm.avail_in = (uInt)input_size;
    strm.next_out = output;
    strm.avail_out = (uInt)output_capacity;

    // Compress in streaming fashion, possibly multiple calls
    while (strm.avail_in > 0 && strm.avail_out > 0) {
        ret = deflate(&strm, Z_NO_FLUSH);
        if (ret != Z_OK) {
            // If we get an error, just finish and clean up
            break;
        }
    }

    // Finish compression
    while (ret == Z_OK) {
        ret = deflate(&strm, Z_FINISH);
        if (ret == Z_STREAM_END) {
            break;
        }
        if (ret != Z_OK) {
            break;
        }
        // If output buffer is full, we need to provide more space, but we allocated enough
        // so this should not happen. Still, break to avoid infinite loop.
        if (strm.avail_out == 0) {
            break;
        }
    }

    // Clean up
    deflateEnd(&strm);
    free(output);

    return 0;
}