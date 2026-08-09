#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <stdlib.h>
#include "zlib.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) {
        return 0;
    }

    // Use first byte to determine number of chunks (2 to 9)
    unsigned int num_chunks = 2 + (data[0] % 8);
    if (size < 1 + num_chunks) {
        return 0;
    }

    // Extract chunk sizes from the next num_chunks bytes
    size_t chunk_sizes[9];
    size_t total_chunk_size = 0;
    for (unsigned int i = 0; i < num_chunks; i++) {
        chunk_sizes[i] = data[1 + i] % 64; // each chunk at most 63 bytes
        total_chunk_size += chunk_sizes[i];
    }

    // Ensure we have enough input data for all chunks
    if (1 + num_chunks + total_chunk_size > size) {
        return 0;
    }

    // Set up z_stream for inflate
    z_stream strm;
    memset(&strm, 0, sizeof(strm));
    if (inflateInit(&strm) != Z_OK) {
        return 0;
    }

    // Feed chunks through the streaming decompressor
    const uint8_t *input_ptr = data + 1 + num_chunks;
    int ret = Z_OK;
    unsigned char outbuf[256];

    for (unsigned int i = 0; i < num_chunks; i++) {
        strm.next_in = (Bytef *)input_ptr;
        strm.avail_in = (uInt)chunk_sizes[i];
        input_ptr += chunk_sizes[i];

        while (strm.avail_in > 0) {
            strm.next_out = outbuf;
            strm.avail_out = sizeof(outbuf);

            ret = inflate(&strm, Z_NO_FLUSH);
            if (ret != Z_OK && ret != Z_STREAM_END && ret != Z_BUF_ERROR) {
                // Error or unexpected return; stop processing
                inflateEnd(&strm);
                return 0;
            }

            if (ret == Z_STREAM_END) {
                // Stream ended; no more input should be processed
                inflateEnd(&strm);
                return 0;
            }

            if (strm.avail_in == 0) {
                break;
            }
        }
    }

    // Finish the stream
    if (ret == Z_OK) {
        strm.next_in = NULL;
        strm.avail_in = 0;
        do {
            strm.next_out = outbuf;
            strm.avail_out = sizeof(outbuf);
            ret = inflate(&strm, Z_FINISH);
            if (ret != Z_OK && ret != Z_STREAM_END && ret != Z_BUF_ERROR) {
                break;
            }
        } while (ret != Z_STREAM_END && strm.avail_out == 0);
    }

    inflateEnd(&strm);
    return 0;
}