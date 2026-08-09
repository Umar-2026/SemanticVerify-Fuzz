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
    uLongf decompressed_len;
    size_t compressed_len;

    if (size == 0) return 0;

    /* Initialize deflate stream */
    memset(&strm, 0, sizeof(strm));
    ret = deflateInit(&strm, Z_DEFAULT_COMPRESSION);
    if (ret != Z_OK) return 0;

    /* Determine upper bound for compressed size */
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
    compressed_len = strm.total_out;

    ret = deflateEnd(&strm);
    if (ret != Z_OK) {
        free(compressed);
        return 0;
    }

    /* Initialize inflate stream */
    memset(&strm, 0, sizeof(strm));
    ret = inflateInit(&strm);
    if (ret != Z_OK) {
        free(compressed);
        return 0;
    }

    /* Prepare decompression buffer */
    decompressed_len = (uLongf)size;
    decompressed = (Bytef *)malloc(size ? size : 1);
    if (decompressed == NULL) {
        inflateEnd(&strm);
        free(compressed);
        return 0;
    }

    /* Decompress */
    strm.next_in = compressed;
    strm.avail_in = (uInt)compressed_len;
    strm.next_out = decompressed;
    strm.avail_out = (uInt)decompressed_len;

    ret = inflate(&strm, Z_FINISH);
    if (ret != Z_STREAM_END) {
        /* Not necessarily an error; just ignore */
    }

    inflateEnd(&strm);
    free(decompressed);
    free(compressed);
    return 0;
}