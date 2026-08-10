#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <stdlib.h>
#include "vpx/vp8dx.h"
#include "vpx/vpx_decoder.h"
#include "vpx/vpx_image.h"

#define CHUNK_SIZE 1024

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size == 0) {
        return 0;
    }

    vpx_codec_ctx_t codec_ctx;
    vpx_codec_dec_cfg_t cfg;
    memset(&cfg, 0, sizeof(cfg));
    cfg.threads = 1;
    cfg.w = 0;
    cfg.h = 0;

    if (vpx_codec_dec_init(&codec_ctx, vpx_codec_vp8_dx(), &cfg, 0) != VPX_CODEC_OK) {
        return 0;
    }

    size_t offset = 0;
    while (offset < size) {
        size_t chunk_len = size - offset;
        if (chunk_len > CHUNK_SIZE) {
            chunk_len = CHUNK_SIZE;
        }

        vpx_codec_err_t err = vpx_codec_decode(&codec_ctx, data + offset, chunk_len, NULL, 0);
        if (err != VPX_CODEC_OK) {
            break;
        }

        vpx_codec_iter_t iter = NULL;
        vpx_image_t *img;
        while ((img = vpx_codec_get_frame(&codec_ctx, &iter)) != NULL) {
            // Consume the frame data to ensure it is processed.
            volatile uint8_t sum = 0;
            for (int plane = 0; plane < 3; plane++) {
                if (img->d_w > 0 && img->d_h > 0) {
                    uint8_t *plane_ptr = img->planes[plane];
                    int stride = img->stride[plane];
                    int h = (plane == 0) ? img->d_h : (img->d_h + 1) / 2;
                    int w = (plane == 0) ? img->d_w : (img->d_w + 1) / 2;
                    for (int y = 0; y < h; y++) {
                        for (int x = 0; x < w; x++) {
                            sum += plane_ptr[y * stride + x];
                        }
                    }
                }
            }
            (void)sum;
        }

        offset += chunk_len;
    }

    vpx_codec_destroy(&codec_ctx);
    return 0;
}