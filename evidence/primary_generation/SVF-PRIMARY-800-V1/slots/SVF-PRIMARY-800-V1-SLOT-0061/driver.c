#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <stdlib.h>
#include "zlib.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

    size_t split = (size_t)data[0] * 256 + data[1];
    if (split > size - 2) split = size - 2;

    const uint8_t *part1_data = data + 2;
    size_t part1_size = split;
    const uint8_t *part2_data = data + 2 + split;
    size_t part2_size = size - 2 - split;

    z_stream strm1, strm2;
    int ret;

    memset(&strm1, 0, sizeof(strm1));
    memset(&strm2, 0, sizeof(strm2));

    ret = inflateInit(&strm1);
    if (ret != Z_OK) return 0;
    ret = inflateInit(&strm2);
    if (ret != Z_OK) {
        inflateEnd(&strm1);
        return 0;
    }

    unsigned char out1[1024];
    unsigned char out2[1024];

    strm1.next_in = (Bytef *)part1_data;
    strm1.avail_in = (uInt)part1_size;
    strm1.next_out = out1;
    strm1.avail_out = sizeof(out1);

    strm2.next_in = (Bytef *)part2_data;
    strm2.avail_in = (uInt)part2_size;
    strm2.next_out = out2;
    strm2.avail_out = sizeof(out2);

    do {
        ret = inflate(&strm1, Z_NO_FLUSH);
        if (ret == Z_STREAM_END) break;
        if (ret != Z_OK && ret != Z_BUF_ERROR) break;
        if (strm1.avail_out == 0) {
            strm1.next_out = out1;
            strm1.avail_out = sizeof(out1);
        }
    } while (strm1.avail_in > 0 || strm1.avail_out == 0);

    do {
        ret = inflate(&strm2, Z_NO_FLUSH);
        if (ret == Z_STREAM_END) break;
        if (ret != Z_OK && ret != Z_BUF_ERROR) break;
        if (strm2.avail_out == 0) {
            strm2.next_out = out2;
            strm2.avail_out = sizeof(out2);
        }
    } while (strm2.avail_in > 0 || strm2.avail_out == 0);

    inflateEnd(&strm1);
    inflateEnd(&strm2);

    return 0;
}