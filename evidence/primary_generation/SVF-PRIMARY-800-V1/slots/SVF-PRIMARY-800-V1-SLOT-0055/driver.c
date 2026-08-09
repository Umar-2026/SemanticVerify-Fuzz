#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <stdlib.h>
#include "zlib.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 8) return 0;

    // Split input: first 4 bytes for dictionary size, next 4 bytes for input size
    uint32_t dict_size_raw = (uint32_t)data[0] | ((uint32_t)data[1] << 8) |
                             ((uint32_t)data[2] << 16) | ((uint32_t)data[3] << 24);
    uint32_t input_size_raw = (uint32_t)data[4] | ((uint32_t)data[5] << 8) |
                              ((uint32_t)data[6] << 16) | ((uint32_t)data[7] << 24);

    size_t remaining = size - 8;
    if (remaining == 0) return 0;

    // Bound dictionary size to remaining bytes, but leave at least 1 byte for input
    size_t dict_size = dict_size_raw % remaining;
    if (dict_size > remaining - 1) dict_size = remaining - 1;
    size_t input_size = remaining - dict_size;
    if (input_size == 0) return 0;

    const uint8_t *dict = data + 8;
    const uint8_t *input = data + 8 + dict_size;

    // Prepare output buffer with generous size
    uLongf out_capacity = compressBound((uLong)input_size) + 1024;
    Bytef *out = (Bytef *)malloc(out_capacity);
    if (!out) return 0;

    z_stream strm;
    memset(&strm, 0, sizeof(strm));

    // Initialize deflate with default compression
    int ret = deflateInit(&strm, Z_DEFAULT_COMPRESSION);
    if (ret != Z_OK) {
        free(out);
        return 0;
    }

    // Set dictionary
    ret = deflateSetDictionary(&strm, (const Bytef *)dict, (uInt)dict_size);
    if (ret != Z_OK) {
        deflateEnd(&strm);
        free(out);
        return 0;
    }

    // Set input
    strm.next_in = (Bytef *)input;
    strm.avail_in = (uInt)input_size;
    strm.next_out = out;
    strm.avail_out = (uInt)out_capacity;

    // Compress in streaming fashion, allowing partial input consumption
    while (strm.avail_in > 0) {
        ret = deflate(&strm, Z_NO_FLUSH);
        if (ret != Z_OK) {
            // If output buffer full, we still continue? For fuzzing, just break on error
            break;
        }
        // If output buffer is full, we could reallocate, but for simplicity break
        if (strm.avail_out == 0) {
            break;
        }
    }

    // Finish compression
    if (ret == Z_OK) {
        do {
            ret = deflate(&strm, Z_FINISH);
        } while (ret == Z_OK);
    }

    deflateEnd(&strm);
    free(out);
    return 0;
}