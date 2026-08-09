#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <stdlib.h>
#include "zlib.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1) return 0;

    z_stream strm;
    memset(&strm, 0, sizeof(strm));

    if (inflateInit(&strm) != Z_OK) {
        return 0;
    }

    // Use first byte to decide windowBits for inflateInit2? No, we already used inflateInit.
    // We'll just use the data as compressed stream.

    strm.next_in = (Bytef *)data;
    strm.avail_in = (uInt)size;

    // Output buffer
    unsigned char out[256];
    int ret;
    int total_out = 0;

    // Feed in chunks to exercise streaming behavior
    size_t consumed = 0;
    while (consumed < size) {
        size_t chunk = size - consumed;
        if (chunk > 64) chunk = 64;
        strm.next_in = (Bytef *)(data + consumed);
        strm.avail_in = (uInt)chunk;
        consumed += chunk;

        do {
            strm.next_out = out;
            strm.avail_out = sizeof(out);
            ret = inflate(&strm, Z_NO_FLUSH);
            total_out += (int)(sizeof(out) - strm.avail_out);

            if (ret == Z_STREAM_END) {
                // Successfully decompressed to end
                inflateEnd(&strm);
                return 0;
            }
            if (ret == Z_NEED_DICT) {
                // Dictionary needed, not supported
                inflateEnd(&strm);
                return 0;
            }
            if (ret == Z_DATA_ERROR || ret == Z_STREAM_ERROR || ret == Z_MEM_ERROR) {
                // Error occurred
                inflateEnd(&strm);
                return 0;
            }
            // Z_OK or Z_BUF_ERROR: continue
        } while (strm.avail_out == 0 && ret != Z_BUF_ERROR);
    }

    // If we get here, stream not finished. Try to finish.
    strm.next_in = NULL;
    strm.avail_in = 0;
    do {
        strm.next_out = out;
        strm.avail_out = sizeof(out);
        ret = inflate(&strm, Z_FINISH);
        total_out += (int)(sizeof(out) - strm.avail_out);
        if (ret == Z_STREAM_END) {
            inflateEnd(&strm);
            return 0;
        }
        if (ret == Z_DATA_ERROR || ret == Z_STREAM_ERROR || ret == Z_MEM_ERROR) {
            inflateEnd(&strm);
            return 0;
        }
        if (ret == Z_NEED_DICT) {
            inflateEnd(&strm);
            return 0;
        }
    } while (strm.avail_out == 0);

    inflateEnd(&strm);
    return 0;
}