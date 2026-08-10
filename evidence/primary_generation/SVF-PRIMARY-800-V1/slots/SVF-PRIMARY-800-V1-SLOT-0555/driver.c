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

    // Parse basic parameters from fuzz input
    unsigned int width = (data[0] << 8) | data[1];
    unsigned int height = (data[2] << 8) | data[3];
    if (width == 0 || height == 0 || width > 4096 || height > 4096) return 0;

    vpx_codec_iface_t *iface = vpx_codec_vp8_cx();
    if (!iface) return 0;

    vpx_codec_enc_cfg_t cfg;
    if (vpx_codec_enc_config_default(iface, &cfg, 0) != VPX_CODEC_OK) return 0;

    cfg.g_w = width;
    cfg.g_h = height;
    cfg.g_timebase.num = 1;
    cfg.g_timebase.den = 30;
    cfg.rc_target_bitrate = 256;

    vpx_codec_ctx_t codec;
    if (vpx_codec_enc_init(&codec, iface, &cfg, 0) != VPX_CODEC_OK) return 0;

    // Prepare image
    vpx_image_t *img = vpx_img_alloc(NULL, VPX_IMG_FMT_I420, width, height, 1);
    if (!img) {
        vpx_codec_destroy(&codec);
        return 0;
    }

    // Fill image planes with fuzz data (bounded)
    size_t offset = 4;
    size_t plane_size_y = (size_t)width * height;
    size_t plane_size_uv = plane_size_y / 4;
    size_t needed = plane_size_y + 2 * plane_size_uv;
    if (offset + needed > size) {
        // Not enough data, fill with zeros
        memset(img->planes[0], 0, plane_size_y);
        memset(img->planes[1], 0, plane_size_uv);
        memset(img->planes[2], 0, plane_size_uv);
    } else {
        memcpy(img->planes[0], data + offset, plane_size_y);
        offset += plane_size_y;
        memcpy(img->planes[1], data + offset, plane_size_uv);
        offset += plane_size_uv;
        memcpy(img->planes[2], data + offset, plane_size_uv);
    }

    // Encode a frame
    vpx_codec_err_t res = vpx_codec_encode(&codec, img, 0, 1, 0, VPX_DL_REALTIME);
    if (res == VPX_CODEC_OK) {
        const vpx_codec_cx_pkt_t *pkt;
        vpx_codec_iter_t iter = NULL;
        while ((pkt = vpx_codec_get_cx_data(&codec, &iter)) != NULL) {
            // Consume packet data (no-op, just ensure it's processed)
        }
    }

    vpx_img_free(img);
    vpx_codec_destroy(&codec);
    return 0;
}