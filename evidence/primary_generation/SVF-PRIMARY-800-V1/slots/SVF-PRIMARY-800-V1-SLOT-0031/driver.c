#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include "zlib.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) {
        return 0;
    }

    // Use the first byte to determine the number of chunks (1 to 8)
    size_t num_chunks = (data[0] % 8) + 1;
    if (num_chunks > size - 1) {
        num_chunks = size - 1;
    }

    // Determine chunk sizes: distribute the remaining bytes among chunks
    size_t remaining = size - 1;
    size_t *chunk_sizes = (size_t *)malloc(num_chunks * sizeof(size_t));
    if (!chunk_sizes) {
        return 0;
    }

    for (size_t i = 0; i < num_chunks; i++) {
        if (i == num_chunks - 1) {
            chunk_sizes[i] = remaining;
        } else {
            // Use data bytes to influence chunk sizes, but ensure at least 1 byte per chunk
            size_t max_chunk = remaining - (num_chunks - i - 1);
            if (max_chunk == 0) {
                max_chunk = 1;
            }
            size_t suggested = data[1 + i] % max_chunk + 1;
            if (suggested > max_chunk) {
                suggested = max_chunk;
            }
            chunk_sizes[i] = suggested;
            remaining -= suggested;
        }
    }

    // Set up z_stream for inflate
    z_stream strm;
    memset(&strm, 0, sizeof(strm));
    if (inflateInit(&strm) != Z_OK) {
        free(chunk_sizes);
        return 0;
    }

    // Feed chunks through the streaming decompressor
    const uint8_t *input_ptr = data + 1;
    size_t input_offset = 0;
    unsigned char outbuf[256];
    int ret = Z_OK;

    for (size_t i = 0; i < num_chunks; i++) {
        size_t chunk_size = chunk_sizes[i];
        if (chunk_size == 0) {
            continue;
        }

        strm.next_in = (Bytef *)(input_ptr + input_offset);
        strm.avail_in = (uInt)chunk_size;
        input_offset += chunk_size;

        // Process all available input in this chunk
        while (strm.avail_in > 0) {
            strm.next_out = outbuf;
            strm.avail_out = sizeof(outbuf);

            ret = inflate(&strm, Z_NO_FLUSH);
            if (ret != Z_OK && ret != Z_STREAM_END && ret != Z_BUF_ERROR) {
                // Error or unexpected return; stop processing
                inflateEnd(&strm);
                free(chunk_sizes);
                return 0;
            }

            if (ret == Z_STREAM_END) {
                // Stream ended; we can stop feeding more chunks
                inflateEnd(&strm);
                free(chunk_sizes);
                return 0;
            }

            // If no progress possible (avail_in unchanged and avail_out full), break to avoid infinite loop
            if (strm.avail_in > 0 && strm.avail_out == 0) {
                continue;
            }
            if (strm.avail_in > 0 && strm.avail_out == sizeof(outbuf)) {
                // No progress; break out of inner loop
                break;
            }
        }
    }

    // Clean up
    inflateEnd(&strm);
    free(chunk_sizes);
    return 0;
}