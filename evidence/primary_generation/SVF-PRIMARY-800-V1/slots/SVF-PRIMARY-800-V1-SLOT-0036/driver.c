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

    size_t chunk_size = data[0] % (size + 1);
    if (chunk_size == 0) chunk_size = 1;

    size_t offset = 1;
    uint8_t out_buffer[4096];

    while (offset < size) {
        size_t remaining = size - offset;
        size_t current_chunk = (remaining < chunk_size) ? remaining : chunk_size;

        strm.next_in = (Bytef *)(data + offset);
        strm.avail_in = (uInt)current_chunk;

        do {
            strm.next_out = out_buffer;
            strm.avail_out = sizeof(out_buffer);

            int ret = inflate(&strm, Z_NO_FLUSH);
            if (ret == Z_STREAM_ERROR || ret == Z_DATA_ERROR || ret == Z_MEM_ERROR) {
                goto cleanup;
            }
            if (ret == Z_STREAM_END) {
                goto cleanup;
            }
        } while (strm.avail_out == 0);

        offset += current_chunk;
    }

cleanup:
    inflateEnd(&strm);
    return 0;
}