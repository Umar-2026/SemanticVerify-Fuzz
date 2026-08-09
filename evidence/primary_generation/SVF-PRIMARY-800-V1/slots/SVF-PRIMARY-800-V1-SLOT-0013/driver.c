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
    int memLevel = (data[3] % 9) + 1;   // 1..9
    int strategy = data[4] % 4;        // Z_DEFAULT_STRATEGY, Z_FILTERED, Z_HUFFMAN_ONLY, Z_RLE
    int flush = data[5] % 6;           // Z_NO_FLUSH, Z_PARTIAL_FLUSH, Z_SYNC_FLUSH, Z_FULL_FLUSH, Z_FINISH, Z_BLOCK
    int chunk_size = (data[6] << 8) | data[7];
    if (chunk_size == 0) chunk_size = 1;
    if (chunk_size > 65536) chunk_size = 65536;

    // Use the rest of the data as input
    const uint8_t *input = data + 8;
    size_t input_size = size - 8;

    // Prepare output buffer (slightly larger than input to avoid overflow)
    size_t output_capacity = input_size + (input_size / 2) + 1024;
    if (output_capacity < 1024) output_capacity = 1024;
    uint8_t *output = (uint8_t *)malloc(output_capacity);
    if (!output) return 0;

    z_stream strm;
    memset(&strm, 0, sizeof(strm));

    // Initialize deflate
    int ret = deflateInit2(&strm, level, method, windowBits, memLevel, strategy);
    if (ret != Z_OK) {
        free(output);
        return 0;
    }

    // Set input
    strm.next_in = (Bytef *)input;
    strm.avail_in = (uInt)input_size;

    // Compress in chunks
    size_t total_out = 0;
    int finished = 0;
    while (strm.avail_in > 0 || !finished) {
        strm.next_out = output + total_out;
        strm.avail_out = (uInt)(output_capacity - total_out);
        if (strm.avail_out == 0) {
            // Expand output buffer if needed
            size_t new_capacity = output_capacity * 2;
            uint8_t *new_output = (uint8_t *)realloc(output, new_capacity);
            if (!new_output) {
                deflateEnd(&strm);
                free(output);
                return 0;
            }
            output = new_output;
            output_capacity = new_capacity;
            strm.next_out = output + total_out;
            strm.avail_out = (uInt)(output_capacity - total_out);
        }

        ret = deflate(&strm, flush);
        if (ret == Z_STREAM_END) {
            finished = 1;
            break;
        }
        if (ret != Z_OK && ret != Z_BUF_ERROR) {
            deflateEnd(&strm);
            free(output);
            return 0;
        }
        total_out = output_capacity - strm.avail_out;
        if (strm.avail_in == 0 && flush != Z_FINISH) {
            // If we've consumed all input and not finishing, we can stop
            break;
        }
    }

    // Clean up
    deflateEnd(&strm);
    free(output);
    return 0;
}