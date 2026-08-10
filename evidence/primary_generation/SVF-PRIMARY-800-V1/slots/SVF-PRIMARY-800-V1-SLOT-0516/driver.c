#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include "vpx/vpx_encoder.h"
#include "vpx/vp8cx.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 128) return 0;

    vpx_codec_ctx_t codec;
    vpx_codec_enc_cfg_t cfg;
    vpx_image_t img;

    if (vpx_codec_enc_config_default(vpx_codec_vp8_cx(), &cfg, 0)) {
        return 0;
    }

    cfg.g_w = 16 + (data[0] % 128);
    cfg.g_h = 16 + (data[1] % 128);
    cfg.g_timebase.num = 1;
    cfg.g_timebase.den = 30;

    if (vpx_codec_enc_init(&codec, vpx_codec_vp8_cx(), &cfg, 0)) {
        return 0;
    }

    if (!vpx_img_alloc(&img, VPX_IMG_FMT_I420, cfg.g_w, cfg.g_h, 1)) {
        vpx_codec_destroy(&codec);
        return 0;
    }

    size_t frame_size = cfg.g_w * cfg.g_h * 3 / 2;
    if (size - 2 >= frame_size) {
        memcpy(img.planes[0], data + 2, cfg.g_w * cfg.g_h);
        memcpy(img.planes[1], data + 2 + (cfg.g_w * cfg.g_h), cfg.g_w * cfg.g_h / 4);
        memcpy(img.planes[2], data + 2 + (cfg.g_w * cfg.g_h) + (cfg.g_w * cfg.g_h / 4), cfg.g_w * cfg.g_h / 4);

        if (vpx_codec_encode(&codec, &img, 0, 1, 0, VPX_DL_REALTIME) == VPX_CODEC_OK) {
            vpx_codec_iter_t iter = NULL;
            const vpx_codec_cx_pkt_t *pkt;
            while ((pkt = vpx_codec_get_cx_data(&codec, &iter)) != NULL) {
                (void)pkt;
            }
        }
    }

    vpx_img_free(&img);
    vpx_codec_destroy(&codec);
    return 0;
}