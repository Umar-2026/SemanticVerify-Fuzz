#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <stdlib.h>
#include "zlib.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    z_stream strm;
    int ret;
    unsigned char out[256];
    size_t consumed = 0;
    int status_seen = 0;

    memset(&strm, 0, sizeof(strm));
    if (inflateInit(&strm) != Z_OK) {
        return 0;
    }

    strm.next_in = (Bytef *)data;
    strm.avail_in = (uInt)(size > UINT_MAX ? UINT_MAX : size);
    consumed = strm.avail_in;

    strm.next_out = out;
    strm.avail_out = sizeof(out);

    ret = inflate(&strm, Z_NO_FLUSH);

    if (ret == Z_STREAM_END) {
        /* Successful decompression to end of stream */
        status_seen = 1;
    } else if (ret == Z_OK) {
        /* More input needed or output produced */
        status_seen = 2;
    } else if (ret == Z_BUF_ERROR) {
        /* No progress possible */
        status_seen = 3;
    } else if (ret == Z_DATA_ERROR) {
        /* Corrupt input */
        status_seen = 4;
    } else if (ret == Z_NEED_DICT) {
        /* Dictionary required */
        status_seen = 5;
    } else if (ret == Z_MEM_ERROR) {
        /* Memory error */
        status_seen = 6;
    } else {
        /* Unknown status */
        status_seen = 7;
    }

    /* Consume remaining input if any */
    if (strm.avail_in > 0) {
        consumed -= strm.avail_in;
    }

    /* Attempt to continue decompression if possible */
    if (ret == Z_OK && strm.avail_out == 0) {
        strm.next_out = out;
        strm.avail_out = sizeof(out);
        ret = inflate(&strm, Z_NO_FLUSH);
        if (ret == Z_STREAM_END) {
            status_seen = 8;
        } else if (ret == Z_BUF_ERROR) {
            status_seen = 9;
        }
    }

    /* Clean up */
    inflateEnd(&strm);

    /* Use status_seen to influence control flow (avoid optimization) */
    if (status_seen == 0) {
        return 0;
    }

    return 0;
}