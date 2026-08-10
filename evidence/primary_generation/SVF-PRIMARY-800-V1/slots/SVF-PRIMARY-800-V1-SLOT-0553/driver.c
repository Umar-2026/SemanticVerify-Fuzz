#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include "vpx/vpx_codec.h"
#include "vpx/vpx_image.h"
#include "vpx/vpx_encoder.h"

#define MAX_IMAGE_SIZE (1024 * 1024)

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 16) return 0;

    // Parse basic parameters from the fuzz input
    unsigned int width = (data[0] << 8) | data[1];
    unsigned int height = (data[2] << 8) | data[3];
    if (width == 0 || height == 0 || width > 4096 || height > 4096) return 0;

    // Determine image format from input
    vpx_img_fmt_t fmt = (vpx_img_fmt_t)(data[4] % 4); // 0=VPX_IMG_FMT_NONE, 1=RGB24, 2=RGB32, 3=YV12
    if (fmt == VPX_IMG_FMT_NONE) fmt = VPX_IMG_FMT_YV12;

    // Allocate image
    vpx_image_t *img = vpx_img_alloc(NULL, fmt, width, height, 1);
    if (!img) return 0;

    // Fill image data with fuzz bytes (bounded)
    size_t plane_size = 0;
    for (int i = 0; i < 3; i++) {
        if (img->planes[i]) {
            plane_size += img->stride[i] * img->d_h;
        }
    }
    if (plane_size > MAX_IMAGE_SIZE) {
        vpx_img_free(img);
        return 0;
    }

    size_t offset = 5;
    for (int i = 0; i < 3; i++) {
        if (img->planes[i]) {
            size_t bytes = img->stride[i] * img->d_h;
            if (offset + bytes > size) {
                // Pad with zeros if not enough data
                memset(img->planes[i], 0, bytes);
            } else {
                memcpy(img->planes[i], data + offset, bytes);
                offset += bytes;
            }
        }
    }

    // Initialize codec context
    vpx_codec_iface_t *iface = vpx_codec_vp8_cx();
    vpx_codec_enc_cfg_t cfg;
    if (vpx_codec_enc_config_default(iface, &cfg, 0) != VPX_CODEC_OK) {
        vpx_img_free(img);
        return 0;
    }

    // Adjust config from fuzz input
    cfg.g_w = width;
    cfg.g_h = height;
    cfg.g_timebase.num = 1;
    cfg.g_timebase.den = 30;
    cfg.g_threads = (data[5] % 4) + 1;
    cfg.rc_target_bitrate = (data[6] << 8) | data[7];

    vpx_codec_ctx_t ctx;
    if (vpx_codec_enc_init(&ctx, iface, &cfg, 0) != VPX_CODEC_OK) {
        vpx_img_free(img);
        return 0;
    }

    // Encode the image
    vpx_codec_err_t res = vpx_codec_encode(&ctx, img, 0, 1, 0, VPX_DL_REALTIME);
    if (res == VPX_CODEC_OK) {
        vpx_codec_iter_t iter = NULL;
        const vpx_codec_cx_pkt_t *pkt;
        while ((pkt = vpx_codec_get_cx_data(&ctx, &iter)) != NULL) {
            // Consume packet data (no-op)
        }
    }

    vpx_codec_destroy(&ctx);
    vpx_img_free(img);
    return 0;
}