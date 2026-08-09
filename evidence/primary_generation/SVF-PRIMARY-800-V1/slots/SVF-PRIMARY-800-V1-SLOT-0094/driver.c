#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include "zlib.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size == 0) return 0;

    z_stream strm;
    strm.zalloc = Z_NULL;
    strm.zfree = Z_NULL;
    strm.opaque = Z_NULL;

    if (deflateInit(&strm, Z_DEFAULT_COMPRESSION) != Z_OK) {
        return 0;
    }

    size_t compressed_size = deflateBound(&strm, size);
    unsigned char *compressed_data = malloc(compressed_size);
    if (!compressed_data) {
        deflateEnd(&strm);
        return 0;
    }

    strm.next_in = (Bytef *)data;
    strm.avail_in = (uInt)size;
    strm.next_out = compressed_data;
    strm.avail_out = (uInt)compressed_size;

    if (deflate(&strm, Z_FINISH) != Z_STREAM_END) {
        free(compressed_data);
        deflateEnd(&strm);
        return 0;
    }
    size_t actual_compressed_size = strm.total_out;
    deflateEnd(&strm);

    z_stream strm_inf;
    strm_inf.zalloc = Z_NULL;
    strm_inf.zfree = Z_NULL;
    strm_inf.opaque = Z_NULL;
    strm_inf.next_in = compressed_data;
    strm_inf.avail_in = (uInt)actual_compressed_size;

    if (inflateInit(&strm_inf) != Z_OK) {
        free(compressed_data);
        return 0;
    }

    unsigned char *decompressed_data = malloc(size + 1);
    if (decompressed_data) {
        strm_inf.next_out = decompressed_data;
        strm_inf.avail_out = (uInt)size;

        inflate(&strm_inf, Z_FINISH);
        free(decompressed_data);
    }

    inflateEnd(&strm_inf);
    free(compressed_data);

    return 0;
}