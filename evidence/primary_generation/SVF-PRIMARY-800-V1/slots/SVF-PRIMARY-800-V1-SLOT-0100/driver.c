#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "zlib.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size == 0) return 0;

    z_stream strm_def;
    z_stream strm_inf;
    
    unsigned char *compressed = malloc(compressBound(size));
    unsigned char *decompressed = malloc(size + 1024);
    if (!compressed || !decompressed) {
        free(compressed);
        free(decompressed);
        return 0;
    }

    strm_def.zalloc = Z_NULL;
    strm_def.zfree = Z_NULL;
    strm_def.opaque = Z_NULL;
    if (deflateInit(&strm_def, Z_DEFAULT_COMPRESSION) != Z_OK) {
        free(compressed);
        free(decompressed);
        return 0;
    }

    strm_def.next_in = (Bytef *)data;
    strm_def.avail_in = (uInt)size;
    strm_def.next_out = compressed;
    strm_def.avail_out = (uInt)compressBound(size);

    if (deflate(&strm_def, Z_FINISH) != Z_STREAM_END) {
        deflateEnd(&strm_def);
        free(compressed);
        free(decompressed);
        return 0;
    }
    uInt compressed_size = strm_def.total_out;
    deflateEnd(&strm_def);

    strm_inf.zalloc = Z_NULL;
    strm_inf.zfree = Z_NULL;
    strm_inf.opaque = Z_NULL;
    strm_inf.next_in = compressed;
    strm_inf.avail_in = compressed_size;
    strm_inf.next_out = decompressed;
    strm_inf.avail_out = (uInt)(size + 1024);

    if (inflateInit(&strm_inf) == Z_OK) {
        inflate(&strm_inf, Z_FINISH);
        inflateEnd(&strm_inf);
    }

    free(compressed);
    free(decompressed);
    return 0;
}