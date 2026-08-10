#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include "vpx/vpx_encoder.h"
#include "vpx/vp8cx.h"
#include "vpx/vpx_image.h"

#define MAX_IMAGE_SIZE (1024 * 1024)
#define MAX_DIM 256

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 8) return 0;

    // Parse dimensions from input
    uint16_t width = (uint16_t)((data[0] << 8) | data[1]);
    uint16_t height = (uint16_t)((data[2] << 8) | data[3]);
    if (width == 0 || height == 0 || width > MAX_DIM || height > MAX_DIM) return 0;

    // Determine bit depth and format
    int bit_depth = (data[4] & 1) ? 10 : 8;
    vpx_img_fmt_t fmt = (data[4] & 2) ? VPX_IMG_FMT_I420 : VPX_IMG_FMT_I420;
    if (bit_depth == 10) fmt = VPX_IMG_FMT_I42016;

    // Allocate image
    vpx_image_t *img = vpx_img_alloc(NULL, fmt, width, height, 1);
    if (!img) return 0;

    // Fill image with fuzz data
    size_t plane_size = (size_t)img->d_w * img->d_h;
    if (bit_depth == 10) plane_size *= 2;
    size_t total_needed = plane_size * 3 / 2; // Y + U + V
    if (size < 8 + total_needed) {
        vpx_img_free(img);
        return 0;
    }

    const uint8_t *p = data + 8;
    for (int plane = 0; plane < 3; plane++) {
        size_t plane_bytes = (plane == 0) ? plane_size : plane_size / 4;
        if (bit_depth == 10) plane_bytes *= 2;
        memcpy(img->planes[plane], p, plane_bytes);
        p += plane_bytes;
    }

    // Initialize encoder
    vpx_codec_ctx_t ctx;
    vpx_codec_enc_cfg_t cfg;
    if (vpx_codec_enc_config_default(vpx_codec_vp8_cx(), &cfg, 0) != VPX_CODEC_OK) {
        vpx_img_free(img);
        return 0;
    }

    cfg.g_w = width;
    cfg.g_h = height;
    cfg.g_bit_depth = bit_depth;
    cfg.g_input_bit_depth = bit_depth;
    cfg.g_timebase.num = 1;
    cfg.g_timebase.den = 30;
    cfg.g_pass = VPX_RC_ONE_PASS;
    cfg.g_lag_in_frames = 0;
    cfg.rc_end_usage = VPX_CBR;
    cfg.rc_target_bitrate = 256;

    if (vpx_codec_enc_init(&ctx, vpx_codec_vp8_cx(), &cfg, 0) != VPX_CODEC_OK) {
        vpx_img_free(img);
        return 0;
    }

    // Encode frame
    vpx_codec_encode(&ctx, img, 0, 1, 0, VPX_DL_REALTIME);

    // Cleanup
    vpx_codec_destroy(&ctx);
    vpx_img_free(img);
    return 0;
}