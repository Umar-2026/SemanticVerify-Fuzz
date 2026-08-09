```c
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
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

    int ret = Z_OK;
    size_t offset = 0;
    size_t chunk_size = 1 + (data[0] % 64);
    size_t num_chunks = 1 + (data[1] % 16);
    size_t chunk_index = 0;

    unsigned char out[256];
    size_t total_in = 0;
    size_t total_out = 0;

    while (chunk_index < num_chunks && offset < size) {
        size_t current_chunk = chunk_size;
        if (offset + current_chunk > size) {
            current_chunk = size - offset;
        }

        strm.next_in = (Bytef *)(data + offset);
        strm.avail_in = (uInt)current_chunk;
        offset += current_chunk;

        do {
            strm.next_out = out;
            strm.avail_out = sizeof(out);

            ret = inflate(&strm, Z_NO_FLUSH);

            total_in += current_chunk - strm.avail_in;
            total_out += sizeof(out) - strm.avail_out;

            if (ret == Z_STREAM_END) {
                break;
            }
            if (ret != Z_OK && ret != Z_BUF_ERROR) {
                break;
            }
        } while (strm.avail_in > 0);

        if (ret == Z_STREAM_END) {
            break;
        }
        if (ret != Z_OK && ret != Z_BUF_ERROR) {
            break;
        }

        chunk_index++;
    }

    inflateEnd(&strm);
    return 0;
}
```