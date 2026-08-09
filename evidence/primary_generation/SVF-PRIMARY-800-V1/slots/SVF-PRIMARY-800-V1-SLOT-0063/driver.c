#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <stdlib.h>
#include "zlib.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

    // Split the input into two parts
    size_t split = (size_t)data[0] * 256 + data[1];
    if (split > size - 2) split = size - 2;
    const uint8_t *part1_data = data + 2;
    size_t part1_size = split;
    const uint8_t *part2_data = data + 2 + split;
    size_t part2_size = size - 2 - split;

    // Initialize two independent z_stream objects
    z_stream strm1, strm2;
    memset(&strm1, 0, sizeof(strm1));
    memset(&strm2, 0, sizeof(strm2));

    // Initialize inflate for both streams
    if (inflateInit(&strm1) != Z_OK) return 0;
    if (inflateInit(&strm2) != Z_OK) {
        inflateEnd(&strm1);
        return 0;
    }

    // Process first part
    unsigned char out1[1024];
    strm1.next_in = (Bytef *)part1_data;
    strm1.avail_in = (uInt)part1_size;
    int ret1 = Z_OK;
    do {
        strm1.next_out = out1;
        strm1.avail_out = sizeof(out1);
        ret1 = inflate(&strm1, Z_NO_FLUSH);
        if (ret1 != Z_OK && ret1 != Z_STREAM_END && ret1 != Z_BUF_ERROR) {
            break;
        }
    } while (strm1.avail_in > 0 && ret1 != Z_STREAM_END);

    // Process second part
    unsigned char out2[1024];
    strm2.next_in = (Bytef *)part2_data;
    strm2.avail_in = (uInt)part2_size;
    int ret2 = Z_OK;
    do {
        strm2.next_out = out2;
        strm2.avail_out = sizeof(out2);
        ret2 = inflate(&strm2, Z_NO_FLUSH);
        if (ret2 != Z_OK && ret2 != Z_STREAM_END && ret2 != Z_BUF_ERROR) {
            break;
        }
    } while (strm2.avail_in > 0 && ret2 != Z_STREAM_END);

    // Clean up
    inflateEnd(&strm1);
    inflateEnd(&strm2);

    return 0;
}