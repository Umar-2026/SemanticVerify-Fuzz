#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <stdlib.h>
#include "zlib.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

    // Use first byte to determine number of chunks (1 to 16)
    size_t num_chunks = (data[0] % 16) + 1;
    if (num_chunks > size - 1) num_chunks = size - 1;

    // Use second byte to determine chunk size variation
    size_t base_chunk = (size - 1) / num_chunks;
    if (base_chunk == 0) base_chunk = 1;

    z_stream strm;
    memset(&strm, 0, sizeof(strm));
    if (inflateInit(&strm) != Z_OK) return 0;

    // Output buffer
    unsigned char outbuf[4096];
    int ret = Z_OK;
    size_t offset = 1; // skip first byte

    for (size_t i = 0; i < num_chunks && offset < size; i++) {
        size_t chunk_size = base_chunk;
        // Vary chunk size based on data byte
        if (offset < size) {
            chunk_size = (data[offset] % base_chunk) + 1;
            if (chunk_size > size - offset) chunk_size = size - offset;
        }

        strm.next_in = (Bytef *)(data + offset);
        strm.avail_in = (uInt)chunk_size;
        offset += chunk_size;

        // Feed the chunk through the stream
        do {
            strm.next_out = outbuf;
            strm.avail_out = sizeof(outbuf);
            ret = inflate(&strm, Z_NO_FLUSH);
            if (ret != Z_OK && ret != Z_STREAM_END && ret != Z_BUF_ERROR) {
                break;
            }
        } while (strm.avail_out == 0 && ret != Z_STREAM_END);

        if (ret != Z_OK && ret != Z_STREAM_END && ret != Z_BUF_ERROR) {
            break;
        }
        if (ret == Z_STREAM_END) {
            // Reset for potential reuse? Not needed, just break
            break;
        }
    }

    // Clean up
    inflateEnd(&strm);
    return 0;
}