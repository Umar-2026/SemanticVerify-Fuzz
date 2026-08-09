#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include "zlib.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) {
        return 0;
    }

    z_stream strm;
    memset(&strm, 0, sizeof(strm));

    if (inflateInit(&strm) != Z_OK) {
        return 0;
    }

    uint8_t out_buffer[4096];
    strm.next_in = (Bytef *)data;
    strm.avail_in = (uInt)size;

    int ret;
    do {
        strm.next_out = out_buffer;
        strm.avail_out = sizeof(out_buffer);

        ret = inflate(&strm, Z_NO_FLUSH);

        switch (ret) {
            case Z_STREAM_END:
                break;
            case Z_OK:
                break;
            case Z_BUF_ERROR:
                break;
            case Z_DATA_ERROR:
                goto cleanup;
            case Z_MEM_ERROR:
                goto cleanup;
            default:
                goto cleanup;
        }
    } while (strm.avail_out == 0);

cleanup:
    inflateEnd(&strm);
    return 0;
}