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

    /* Use the first byte to determine the windowBits for decompression mode */
    /* 15 + 16 = gzip, 15 = zlib, -15 = raw */
    int windowBits = 15;
    uint8_t mode_selector = data[0];
    if (mode_selector < 85) {
        windowBits = 15;
    } else if (mode_selector < 170) {
        windowBits = 15 + 16;
    } else {
        windowBits = -15;
    }

    if (inflateInit2(&strm, windowBits) != Z_OK) {
        return 0;
    }

    uint8_t buffer[4096];
    strm.next_in = (Bytef *)(data + 1);
    strm.avail_in = (uInt)(size - 1);

    /* Stream decompression in chunks */
    do {
        strm.next_out = buffer;
        strm.avail_out = sizeof(buffer);
        
        int ret = inflate(&strm, Z_NO_FLUSH);
        if (ret == Z_STREAM_END || ret == Z_DATA_ERROR || ret == Z_MEM_ERROR || ret == Z_BUF_ERROR) {
            break;
        }
    } while (strm.avail_out == 0);

    inflateEnd(&strm);
    return 0;
}