#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <stdlib.h>
#include "zlib.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    z_stream strm;
    int ret;
    unsigned char *out;
    size_t out_size = 64 * 1024;
    size_t total_out = 0;

    if (size == 0) {
        return 0;
    }

    out = (unsigned char *)malloc(out_size);
    if (out == NULL) {
        return 0;
    }

    memset(&strm, 0, sizeof(strm));
    if (inflateInit(&strm) != Z_OK) {
        free(out);
        return 0;
    }

    strm.next_in = (Bytef *)data;
    strm.avail_in = (uInt)size;

    do {
        strm.next_out = out;
        strm.avail_out = (uInt)out_size;
        ret = inflate(&strm, Z_NO_FLUSH);
        total_out += out_size - strm.avail_out;
        if (ret == Z_STREAM_ERROR || ret == Z_NEED_DICT || ret == Z_DATA_ERROR || ret == Z_MEM_ERROR) {
            break;
        }
    } while (ret != Z_STREAM_END && strm.avail_in > 0);

    inflateEnd(&strm);
    free(out);
    return 0;
}