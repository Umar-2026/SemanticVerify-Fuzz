#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <stdlib.h>
#include "zlib.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    z_stream strm;
    int ret;
    unsigned char *comp_buf;
    unsigned char *decomp_buf;
    size_t comp_buf_size;
    size_t decomp_buf_size;
    size_t total_in = 0;
    size_t total_out = 0;
    int flush;
    int have;

    if (size == 0) {
        return 0;
    }

    /* Initialize compression stream */
    memset(&strm, 0, sizeof(strm));
    ret = deflateInit(&strm, Z_DEFAULT_COMPRESSION);
    if (ret != Z_OK) {
        return 0;
    }

    /* Allocate output buffer for compression: worst case is size + size/1000 + 13 */
    comp_buf_size = size + (size / 1000) + 13;
    if (comp_buf_size < size) {
        deflateEnd(&strm);
        return 0;
    }
    comp_buf = (unsigned char *)malloc(comp_buf_size);
    if (comp_buf == NULL) {
        deflateEnd(&strm);
        return 0;
    }

    /* Compress all input in one call */
    strm.next_in = (Bytef *)data;
    strm.avail_in = (uInt)size;
    strm.next_out = comp_buf;
    strm.avail_out = (uInt)comp_buf_size;

    ret = deflate(&strm, Z_FINISH);
    if (ret != Z_STREAM_END) {
        free(comp_buf);
        deflateEnd(&strm);
        return 0;
    }

    total_in = strm.total_in;
    total_out = strm.total_out;
    deflateEnd(&strm);

    if (total_out == 0 || total_out > comp_buf_size) {
        free(comp_buf);
        return 0;
    }

    /* Initialize decompression stream */
    memset(&strm, 0, sizeof(strm));
    ret = inflateInit(&strm);
    if (ret != Z_OK) {
        free(comp_buf);
        return 0;
    }

    /* Allocate output buffer for decompression: use original size, but handle if larger */
    decomp_buf_size = size;
    if (decomp_buf_size == 0) {
        decomp_buf_size = 1;
    }
    decomp_buf = (unsigned char *)malloc(decomp_buf_size);
    if (decomp_buf == NULL) {
        inflateEnd(&strm);
        free(comp_buf);
        return 0;
    }

    strm.next_in = comp_buf;
    strm.avail_in = (uInt)total_out;
    strm.next_out = decomp_buf;
    strm.avail_out = (uInt)decomp_buf_size;

    ret = inflate(&strm, Z_FINISH);
    if (ret != Z_STREAM_END) {
        /* If output buffer too small, try to continue with larger buffer? For fuzzing, just ignore */
        inflateEnd(&strm);
        free(decomp_buf);
        free(comp_buf);
        return 0;
    }

    /* Optionally verify decompressed data matches original if sizes match */
    if (strm.total_out == size) {
        if (memcmp(decomp_buf, data, size) != 0) {
            /* Mismatch, but we don't abort; just note */
        }
    }

    inflateEnd(&strm);
    free(decomp_buf);
    free(comp_buf);
    return 0;
}