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
    Bytef *decompressed = NULL;
    uLong compressed_size;
    uLong decompressed_size;
    size_t total_in = 0;
    size_t total_out = 0;
    int flush;
    int have;
    int err;

    if (size == 0) {
        return 0;
    }

    /* Initialize deflate stream */
    memset(&strm, 0, sizeof(strm));
    ret = deflateInit(&strm, Z_DEFAULT_COMPRESSION);
    if (ret != Z_OK) {
        return 0;
    }

    /* Allocate output buffer for compression */
    bound = deflateBound(&strm, (uLong)size);
    compressed = (Bytef *)malloc(bound);
    if (compressed == NULL) {
        deflateEnd(&strm);
        return 0;
    }

    /* Compress input in chunks */
    strm.next_in = (Bytef *)data;
    strm.avail_in = (uInt)size;
    strm.next_out = compressed;
    strm.avail_out = (uInt)bound;

    do {
        flush = (strm.avail_in == 0) ? Z_FINISH : Z_NO_FLUSH;
        ret = deflate(&strm, flush);
        if (ret == Z_STREAM_ERROR) {
            free(compressed);
            deflateEnd(&strm);
            return 0;
        }
        if (ret == Z_BUF_ERROR && strm.avail_in > 0) {
            /* Should not happen with enough output space, but handle */
            free(compressed);
            deflateEnd(&strm);
            return 0;
        }
    } while (strm.avail_in > 0 || (flush == Z_FINISH && ret != Z_STREAM_END));

    if (ret != Z_STREAM_END) {
        free(compressed);
        deflateEnd(&strm);
        return 0;
    }

    compressed_size = (uLong)(strm.total_out);
    deflateEnd(&strm);

    /* Initialize inflate stream */
    memset(&strm, 0, sizeof(strm));
    ret = inflateInit(&strm);
    if (ret != Z_OK) {
        free(compressed);
        return 0;
    }

    /* Allocate decompression buffer */
    decompressed_size = (uLong)size + 1; /* +1 for safety */
    decompressed = (Bytef *)malloc(decompressed_size);
    if (decompressed == NULL) {
        inflateEnd(&strm);
        free(compressed);
        return 0;
    }

    /* Decompress */
    strm.next_in = compressed;
    strm.avail_in = (uInt)compressed_size;
    strm.next_out = decompressed;
    strm.avail_out = (uInt)decompressed_size;

    do {
        ret = inflate(&strm, Z_NO_FLUSH);
        if (ret == Z_STREAM_ERROR || ret == Z_NEED_DICT || ret == Z_DATA_ERROR || ret == Z_MEM_ERROR) {
            break;
        }
        if (ret == Z_BUF_ERROR && strm.avail_in == 0) {
            /* Not enough input, but we have all input, so this is an error */
            break;
        }
    } while (ret != Z_STREAM_END && strm.avail_in > 0);

    if (ret != Z_STREAM_END) {
        /* Decompression failed, but we still free resources */
    }

    inflateEnd(&strm);
    free(decompressed);
    free(compressed);

    return 0;
}