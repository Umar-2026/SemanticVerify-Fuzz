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
        /* Fully decompressed stream */
        inflateEnd(&strm);
        return 1;
    } else if (ret == Z_OK) {
        /* More input needed or output produced */
        if (strm.avail_in == 0 && strm.avail_out == sizeof(out)) {
            /* No progress, likely need more input */
            inflateEnd(&strm);
            return 2;
        } else {
            /* Some output produced, continue */
            inflateEnd(&strm);
            return 3;
        }
    } else if (ret == Z_BUF_ERROR) {
        /* No progress possible */
        inflateEnd(&strm);
        return 4;
    } else if (ret == Z_DATA_ERROR) {
        /* Corrupt input */
        inflateEnd(&strm);
        return 5;
    } else if (ret == Z_MEM_ERROR) {
        /* Memory allocation failure */
        inflateEnd(&strm);
        return 6;
    } else if (ret == Z_NEED_DICT) {
        /* Dictionary required */
        inflateEnd(&strm);
        return 7;
    } else {
        /* Unexpected status */
        inflateEnd(&strm);
        return 8;
    }
}