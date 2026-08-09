#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <stdlib.h>
#include "zlib.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    z_stream strm;
    int ret;
    uLong bound;
    Bytef *compressed = NULL;
    uLongf compressed_len;
    Bytef *decompressed = NULL;
    uLongf decompressed_len;

    if (size == 0) {
        return 0;
    }

    /* Initialize deflate stream */
    memset(&strm, 0, sizeof(strm));
    ret = deflateInit(&strm, Z_DEFAULT_COMPRESSION);
    if (ret != Z_OK) {
        return 0;
    }

    /* Allocate output buffer for compressed data */
    bound = deflateBound(&strm, (uLong)size);
    compressed = (Bytef *)malloc(bound);
    if (compressed == NULL) {
        deflateEnd(&strm);
        return 0;
    }

    strm.next_in = (Bytef *)data;
    strm.avail_in = (uInt)size;
    strm.next_out = compressed;
    strm.avail_out = (uInt)bound;

    /* Compress all input */
    ret = deflate(&strm, Z_FINISH);
    if (ret != Z_STREAM_END) {
        free(compressed);
        deflateEnd(&strm);
        return 0;
    }

    compressed_len = (uLongf)(strm.total_out);
    deflateEnd(&strm);

    /* Initialize inflate stream */
    memset(&strm, 0, sizeof(strm));
    ret = inflateInit(&strm);
    if (ret != Z_OK) {
        free(compressed);
        return 0;
    }

    /* Allocate output buffer for decompressed data */
    decompressed_len = (uLongf)size;
    decompressed = (Bytef *)malloc((size_t)decompressed_len);
    if (decompressed == NULL) {
        inflateEnd(&strm);
        free(compressed);
        return 0;
    }

    strm.next_in = compressed;
    strm.avail_in = (uInt)compressed_len;
    strm.next_out = decompressed;
    strm.avail_out = (uInt)decompressed_len;

    /* Decompress */
    ret = inflate(&strm, Z_FINISH);
    if (ret != Z_STREAM_END) {
        /* Not necessarily an error; just ignore */
    }

    inflateEnd(&strm);
    free(decompressed);
    free(compressed);

    return 0;
}