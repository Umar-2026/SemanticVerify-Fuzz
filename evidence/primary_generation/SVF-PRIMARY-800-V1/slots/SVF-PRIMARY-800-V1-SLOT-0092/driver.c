#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "zlib.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size == 0) return 0;

    z_stream strm_def;
    z_stream strm_inf;
    
    memset(&strm_def, 0, sizeof(strm_def));
    memset(&strm_inf, 0, sizeof(strm_inf));

    if (deflateInit(&strm_def, Z_DEFAULT_COMPRESSION) != Z_OK) return 0;
    if (inflateInit(&strm_inf) != Z_OK) {
        deflateEnd(&strm_def);
        return 0;
    }

    size_t max_out = deflateBound(&strm_def, size);
    uint8_t *compressed = malloc(max_out);
    uint8_t *decompressed = malloc(size + 1024);

    if (!compressed || !decompressed) {
        free(compressed);
        free(decompressed);
        deflateEnd(&strm_def);
        inflateEnd(&strm_inf);
        return 0;
    }

    strm_def.next_in = (Bytef *)data;
    strm_def.avail_in = (uInt)size;
    strm_def.next_out = compressed;
    strm_def.avail_out = (uInt)max_out;

    if (deflate(&strm_def, Z_FINISH) == Z_STREAM_END) {
        strm_inf.next_in = compressed;
        strm_inf.avail_in = (uInt)(max_out - strm_def.avail_out);
        strm_inf.next_out = decompressed;
        strm_inf.avail_out = (uInt)(size + 1024);

        inflate(&strm_inf, Z_FINISH);
    }

    deflateEnd(&strm_def);
    inflateEnd(&strm_inf);
    free(compressed);
    free(decompressed);

    return 0;
}