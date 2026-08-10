#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include "vpx/vp8dx.h"
#include "vpx/vpx_decoder.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    vpx_codec_ctx_t codec;
    vpx_codec_dec_cfg_t cfg;
    memset(&cfg, 0, sizeof(cfg));
    cfg.threads = 1;

    if (vpx_codec_dec_init(&codec, vpx_codec_vp8_dx(), &cfg, 0) != VPX_CODEC_OK) {
        return 0;
    }

    vpx_codec_decode(&codec, data, size, NULL, 0);

    vpx_codec_iter_t iter = NULL;
    vpx_image_t *img;
    while ((img = vpx_codec_get_frame(&codec, &iter)) != NULL) {
        // Consume frame data to prevent optimization
        volatile uint8_t sum = 0;
        for (int plane = 0; plane < 3; plane++) {
            const uint8_t *buf = img->planes[plane];
            const int stride = img->stride[plane];
            const int h = (plane == 0) ? img->d_h : (img->d_h + 1) / 2;
            for (int y = 0; y < h; y++) {
                for (int x = 0; x < stride; x++) {
                    sum += buf[y * stride + x];
                }
            }
        }
        (void)sum;
    }

    vpx_codec_destroy(&codec);
    return 0;
}