#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <stdlib.h>
#include "zlib.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    z_stream strm;
    int ret;
    unsigned char out[1024];

    if (size == 0) {
        return 0;
    }

    memset(&strm, 0, sizeof(strm));
    if (inflateInit(&strm) != Z_OK) {
        return 0;
    }

    strm.next_in = (Bytef *)data;
    strm.avail_in = (uInt)size;

    do {
        strm.next_out = out;
        strm.avail_out = sizeof(out);
        ret = inflate(&strm, Z_NO_FLUSH);
        if (ret != Z_OK && ret != Z_STREAM_END && ret != Z_BUF_ERROR) {
            break;
        }
    } while (ret != Z_STREAM_END && strm.avail_in > 0);

    inflateEnd(&strm);
    return 0;
}