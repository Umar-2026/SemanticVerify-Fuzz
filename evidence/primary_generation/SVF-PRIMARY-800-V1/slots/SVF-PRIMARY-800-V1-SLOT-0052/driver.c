#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include "zlib.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 16) {
        return 0;
    }

    size_t dict_size = data[0] % (size / 2 + 1);
    size_t input_size = size - dict_size - 1;
    const uint8_t *dict = data + 1;
    const uint8_t *input = data + 1 + dict_size;

    z_stream strm;
    memset(&strm, 0, sizeof(strm));

    if (deflateInit(&strm, Z_DEFAULT_COMPRESSION) != Z_OK) {
        return 0;
    }

    if (deflateSetDictionary(&strm, dict, (uInt)dict_size) != Z_OK) {
        deflateEnd(&strm);
        return 0;
    }

    uint8_t *out_buf = malloc(deflateBound(&strm, (uLong)input_size));
    if (!out_buf) {
        deflateEnd(&strm);
        return 0;
    }

    strm.next_in = (Bytef *)input;
    strm.avail_in = (uInt)input_size;
    strm.next_out = out_buf;
    strm.avail_out = (uInt)deflateBound(&strm, (uLong)input_size);

    deflate(&strm, Z_FINISH);
    deflateEnd(&strm);
    free(out_buf);

    return 0;
}