#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include "vpx/vpx_encoder.h"
#include "vpx/vp8cx.h"
#include "vpx/vpx_image.h"

#define MAX_IMAGE_SIZE (1024 * 1024)

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 4) return 0;

    // Parse dimensions from input
    uint16_t width = (uint16_t)((data[0] << 8) | data[1]);
    uint16_t height = (uint16_t)((data[2] << 8) | data[3]);
    if (width == 0 || height == 0 || width > 4096 || height > 4096) return 0;

    // Determine pixel format from next byte
    vpx_img_fmt_t fmt;
    if (size < 5) return 0;
    switch (data[4] % 4) {
        case 0: fmt = VPX_IMG_FMT_I420; break;
        case 1: fmt = VPX_IMG_FMT_I422; break;
        case 2: fmt = VPX_IMG_FMT_I444; break;
        default: fmt = VPX_IMG_FMT_YV12; break;
    }

    // Allocate image
    vpx_image_t *img = vpx_img_alloc(NULL, fmt, width, height, 1);
    if (!img) return 0;

    // Fill image planes with fuzz data
    size_t offset = 5;
    for (int plane = 0; plane < 3; plane++) {
        size_t plane_size = img->stride[plane] * img->d_h;
        if (offset + plane_size > size) {
            // Fill remaining with zeros
            memset(img->planes[plane], 0, plane_size);
        } else {
            memcpy(img->planes[plane], data + offset, plane_size);
            offset += plane_size;
        }
    }

    // Initialize encoder configuration
    vpx_codec_enc_cfg_t cfg;
    if (vpx_codec_enc_config_default(vpx_codec_vp8_cx(), &cfg, 0) != VPX_CODEC_OK) {
        vpx_img_free(img);
        return 0;
    }

    cfg.g_w = width;
    cfg.g_h = height;
    cfg.g_timebase.num = 1;
    cfg.g_timebase.den = 30;
    cfg.rc_target_bitrate = 256;

    // Create encoder context
    vpx_codec_ctx_t ctx;
    if (vpx_codec_enc_init(&ctx, vpx_codec_vp8_cx(), &cfg, 0) != VPX_CODEC_OK) {
        vpx_img_free(img);
        return 0;
    }

    // Encode the image
    vpx_codec_err_t res = vpx_codec_encode(&ctx, img, 0, 1, 0, VPX_DL_REALTIME);
    if (res == VPX_CODEC_OK) {
        // Consume any output packets
        const vpx_codec_cx_pkt_t *pkt;
        vpx_codec_iter_t iter = NULL;
        while ((pkt = vpx_codec_get_cx_data(&ctx, &iter)) != NULL) {
            // Just iterate through packets
        }
    }

    // Cleanup
    vpx_codec_destroy(&ctx);
    vpx_img_free(img);

    return 0;
}