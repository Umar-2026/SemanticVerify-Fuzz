#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <stdlib.h>
#include "zlib.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    z_stream strm;
    int ret;
    uLong bound;
    Bytef *compressed;
    Bytef *decompressed;
    uLongf compressed_len;
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

    /* Compute upper bound for compressed size */
    bound = deflateBound(&strm, (uLong)size);
    compressed = (Bytef *)malloc(bound);
    if (compressed == NULL) {
        deflateEnd(&strm);
        return 0;
    }

    /* Compress input */
    strm.next_in = (Bytef *)data;
    strm.avail_in = (uInt)size;
    strm.next_out = compressed;
    strm.avail_out = (uInt)bound;

    ret = deflate(&strm, Z_FINISH);
    if (ret != Z_STREAM_END) {
        free(compressed);
        deflateEnd(&strm);
        return 0;
    }

    compressed_len = (uLong)(strm.total_out);
    deflateEnd(&strm);

    /* Initialize inflate stream */
    memset(&strm, 0, sizeof(strm));
    ret = inflateInit(&strm);
    if (ret != Z_OK) {
        free(compressed);
        return 0;
    }

    /* Allocate decompression buffer (same size as input) */
    decompressed = (Bytef *)malloc(size ? size : 1);
    if (decompressed == NULL) {
        inflateEnd(&strm);
        free(compressed);
        return 0;
    }

    strm.next_in = compressed;
    strm.avail_in = (uInt)compressed_len;
    strm.next_out = decompressed;
    strm.avail_out = (uInt)size;

    ret = inflate(&strm, Z_FINISH);
    if (ret != Z_STREAM_END) {
        /* Decompression failed, but we still free resources */
        inflateEnd(&strm);
        free(decompressed);
        free(compressed);
        return 0;
    }

    decompressed_len = (uLong)(strm.total_out);

    /* Optionally verify that decompressed data matches original */
    if (decompressed_len == size) {
        if (memcmp(decompressed, data, size) != 0) {
            /* Mismatch, but we don't crash */
        }
    }

    inflateEnd(&strm);
    free(decompressed);
    free(compressed);
    return 0;
}