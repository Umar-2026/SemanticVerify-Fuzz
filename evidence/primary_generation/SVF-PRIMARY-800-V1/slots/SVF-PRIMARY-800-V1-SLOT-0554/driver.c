#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include "vpx/vpx_encoder.h"
#include "vpx/vp8cx.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 16) return 0;

    vpx_codec_ctx_t codec;
    vpx_codec_enc_cfg_t cfg;
    vpx_image_t img;

    vpx_codec_enc_config_default(vpx_codec_vp8_cx(), &cfg, 0);
    cfg.g_w = 16;
    cfg.g_h = 16;
    cfg.g_timebase.num = 1;
    cfg.g_timebase.den = 30;

    if (vpx_codec_enc_init(&codec, vpx_codec_vp8_cx(), &cfg, 0) != VPX_CODEC_OK) {
        return 0;
    }

    if (vpx_img_alloc(&img, VPX_IMG_FMT_I420, cfg.g_w, cfg.g_h, 1)) {
        size_t plane_size = cfg.g_w * cfg.g_h;
        size_t uv_size = (cfg.g_w / 2) * (cfg.g_h / 2);

        if (size >= plane_size + 2 * uv_size) {
            memcpy(img.planes[VPX_PLANE_Y], data, plane_size);
            memcpy(img.planes[VPX_PLANE_U], data + plane_size, uv_size);
            memcpy(img.planes[VPX_PLANE_V], data + plane_size + uv_size, uv_size);

            vpx_codec_encode(&codec, &img, 0, 1, 0, VPX_DL_REALTIME);
        }

        vpx_img_free(&img);
    }

    vpx_codec_destroy(&codec);
    return 0;
}