#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <stdlib.h>
#include "vpx/vp8dx.h"
#include "vpx/vpx_decoder.h"
#include "vpx/vpx_image.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1) return 0;

    vpx_codec_ctx_t codec_ctx;
    vpx_codec_dec_cfg_t cfg = {0, 0, 0};
    if (vpx_codec_dec_init(&codec_ctx, vpx_codec_vp8_dx(), &cfg, 0) != VPX_CODEC_OK) {
        return 0;
    }

    // Split input into chunks: first byte determines number of chunks (1-16)
    size_t num_chunks = (data[0] % 16) + 1;
    if (num_chunks > size) num_chunks = size;
    size_t chunk_size = (size - 1) / num_chunks;
    if (chunk_size == 0) chunk_size = 1;

    const uint8_t *ptr = data + 1;
    size_t remaining = size - 1;

    for (size_t i = 0; i < num_chunks && remaining > 0; i++) {
        size_t cur_size = chunk_size;
        if (cur_size > remaining) cur_size = remaining;

        if (vpx_codec_decode(&codec_ctx, ptr, cur_size, NULL, 0) != VPX_CODEC_OK) {
            // Decode error, but continue with remaining chunks
            ptr += cur_size;
            remaining -= cur_size;
            continue;
        }

        // Retrieve any available frames
        vpx_codec_iter_t iter = NULL;
        vpx_image_t *img;
        while ((img = vpx_codec_get_frame(&codec_ctx, &iter)) != NULL) {
            // Consume frame data (just touch it to prevent optimization)
            volatile uint8_t sum = 0;
            for (int plane = 0; plane < 3; plane++) {
                if (img->planes[plane] && img->d_w && img->d_h) {
                    for (unsigned int y = 0; y < img->d_h; y++) {
                        const uint8_t *row = img->planes[plane] + y * img->stride[plane];
                        for (unsigned int x = 0; x < img->d_w; x++) {
                            sum += row[x];
                        }
                    }
                }
            }
            (void)sum;
        }

        ptr += cur_size;
        remaining -= cur_size;
    }

    // Flush decoder
    vpx_codec_decode(&codec_ctx, NULL, 0, NULL, 0);
    vpx_codec_iter_t iter = NULL;
    vpx_image_t *img;
    while ((img = vpx_codec_get_frame(&codec_ctx, &iter)) != NULL) {
        // Consume frame data
        volatile uint8_t sum = 0;
        for (int plane = 0; plane < 3; plane++) {
            if (img->planes[plane] && img->d_w && img->d_h) {
                for (unsigned int y = 0; y < img->d_h; y++) {
                    const uint8_t *row = img->planes[plane] + y * img->stride[plane];
                    for (unsigned int x = 0; x < img->d_w; x++) {
                        sum += row[x];
                    }
                }
            }
        }
        (void)sum;
    }

    vpx_codec_destroy(&codec_ctx);
    return 0;
}