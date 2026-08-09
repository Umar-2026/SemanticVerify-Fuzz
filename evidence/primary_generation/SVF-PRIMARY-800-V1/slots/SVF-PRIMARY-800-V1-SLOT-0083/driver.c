#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <stdlib.h>
#include "zlib.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

    z_stream strm;
    memset(&strm, 0, sizeof(strm));

    if (inflateInit(&strm) != Z_OK) {
        return 0;
    }

    /* Use first byte to choose windowBits for inflateInit2? Not needed; we use inflateInit. */
    /* Use second byte to decide flush mode and chunking behavior. */
    int flush_mode = data[1] % 3; /* 0: Z_NO_FLUSH, 1: Z_SYNC_FLUSH, 2: Z_FINISH */
    int flush;
    switch (flush_mode) {
        case 0: flush = Z_NO_FLUSH; break;
        case 1: flush = Z_SYNC_FLUSH; break;
        default: flush = Z_FINISH; break;
    }

    /* Feed input in chunks, varying chunk size based on data[0] */
    size_t chunk_size = (size_t)(data[0] % 64) + 1;
    if (chunk_size > size - 2) chunk_size = size - 2;

    const uint8_t *input = data + 2;
    size_t input_len = size - 2;

    size_t consumed = 0;
    int ret = Z_OK;
    int status_seen = 0;

    /* Output buffer */
    unsigned char outbuf[256];
    size_t total_out = 0;

    strm.next_in = (Bytef *)input;
    strm.avail_in = 0;

    while (consumed < input_len || strm.avail_in > 0) {
        if (strm.avail_in == 0 && consumed < input_len) {
            size_t to_feed = chunk_size;
            if (to_feed > input_len - consumed) to_feed = input_len - consumed;
            strm.next_in = (Bytef *)(input + consumed);
            strm.avail_in = (uInt)to_feed;
            consumed += to_feed;
        }

        strm.next_out = outbuf;
        strm.avail_out = sizeof(outbuf);

        ret = inflate(&strm, flush);

        if (ret == Z_STREAM_END) {
            status_seen = 1;
            break;
        } else if (ret == Z_BUF_ERROR) {
            /* No progress possible; if we have no input and not finished, break */
            if (strm.avail_in == 0 && consumed >= input_len) {
                break;
            }
            /* Otherwise continue to feed more input */
        } else if (ret == Z_DATA_ERROR || ret == Z_MEM_ERROR || ret == Z_NEED_DICT) {
            status_seen = 1;
            break;
        } else if (ret != Z_OK) {
            /* Unexpected status */
            status_seen = 1;
            break;
        }

        total_out += sizeof(outbuf) - strm.avail_out;

        /* If we consumed all input and avail_in == 0 and ret == Z_OK, we might need to loop to flush */
        if (strm.avail_in == 0 && consumed >= input_len && flush != Z_FINISH) {
            /* Continue to allow inflate to process internal state */
        }
    }

    /* Ensure we've seen at least one status code */
    if (!status_seen && ret == Z_OK) {
        /* Do a final call to get a status */
        strm.next_out = outbuf;
        strm.avail_out = sizeof(outbuf);
        ret = inflate(&strm, Z_FINISH);
        if (ret == Z_STREAM_END || ret == Z_BUF_ERROR || ret == Z_DATA_ERROR) {
            status_seen = 1;
        }
    }

    /* Different functional outcomes based on ret */
    if (ret == Z_STREAM_END) {
        /* Successful decompression */
        volatile int result = 1;
        (void)result;
    } else if (ret == Z_DATA_ERROR) {
        /* Corrupt data */
        volatile int result = 2;
        (void)result;
    } else if (ret == Z_MEM_ERROR) {
        /* Memory error */
        volatile int result = 3;
        (void)result;
    } else if (ret == Z_NEED_DICT) {
        /* Dictionary needed */
        volatile int result = 4;
        (void)result;
    } else if (ret == Z_BUF_ERROR) {
        /* Buffer error */
        volatile int result = 5;
        (void)result;
    } else {
        /* Z_OK or other */
        volatile int result = 6;
        (void)result;
    }

    inflateEnd(&strm);
    return 0;
}