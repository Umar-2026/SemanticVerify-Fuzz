#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <stdlib.h>
#include "zlib.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

    // Use first byte to determine number of chunks (1 to 8)
    size_t num_chunks = (data[0] % 8) + 1;
    if (num_chunks > size - 1) num_chunks = size - 1;

    // Use second byte to determine chunk size variation
    size_t base_chunk = (size - 1) / num_chunks;
    if (base_chunk == 0) base_chunk = 1;

    z_stream strm;
    memset(&strm, 0, sizeof(strm));
    if (inflateInit(&strm) != Z_OK) return 0;

    const uint8_t *input = data + 1;
    size_t remaining = size - 1;
    int ret = Z_OK;

    for (size_t i = 0; i < num_chunks && remaining > 0; i++) {
        size_t chunk_size = base_chunk;
        // Vary chunk size slightly based on input byte
        if (i < num_chunks - 1 && remaining > chunk_size) {
            chunk_size = (data[0] + i) % (remaining / (num_chunks - i)) + 1;
            if (chunk_size > remaining) chunk_size = remaining;
        } else {
            chunk_size = remaining;
        }

        strm.next_in = (Bytef *)input;
        strm.avail_in = (uInt)chunk_size;

        // Output buffer
        unsigned char out[256];
        do {
            strm.next_out = out;
            strm.avail_out = sizeof(out);
            ret = inflate(&strm, Z_NO_FLUSH);
            if (ret != Z_OK && ret != Z_STREAM_END && ret != Z_BUF_ERROR) {
                break;
            }
        } while (strm.avail_out == 0 && ret != Z_STREAM_END);

        input += chunk_size;
        remaining -= chunk_size;

        if (ret == Z_STREAM_END) break;
        if (ret != Z_OK && ret != Z_BUF_ERROR) break;
    }

    inflateEnd(&strm);
    return 0;
}