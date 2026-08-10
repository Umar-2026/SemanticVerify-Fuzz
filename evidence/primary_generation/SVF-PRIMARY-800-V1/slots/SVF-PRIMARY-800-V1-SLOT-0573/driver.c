#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include "vpx/vpx_encoder.h"
#include "vpx/vp8cx.h"
#include "vpx/vpx_image.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 8) return 0;

    // Parse dimensions from input
    unsigned int width = (data[0] << 8) | data[1];
    unsigned int height = (data[2] << 8) | data[3];
    if (width == 0 || height == 0 || width > 4096 || height > 4096) return 0;

    // Determine bit depth and flags
    int bit_depth = 8;
    vpx_img_fmt_t fmt = VPX_IMG_FMT_I420;
    unsigned int flags = 0;
    if (data[4] & 0x01) {
        bit_depth = 10;
        fmt = VPX_IMG_FMT_I42016;
        flags |= VPX_IMG_FLAG_HIGHBITDEPTH;
    }

    // Allocate image
    vpx_image_t *img = vpx_img_alloc(NULL, fmt, width, height, 1);
    if (!img) return 0;

    // Fill image planes with fuzz data
    size_t offset = 8;
    size_t plane_size = (size_t)img->stride[0] * img->d_h;
    if (offset + plane_size > size) {
        vpx_img_free(img);
        return 0;
    }
    memcpy(img->planes[0], data + offset, plane_size);
    offset += plane_size;

    plane_size = (size_t)img->stride[1] * ((img->d_h + 1) / 2);
    if (offset + plane_size > size) {
        vpx_img_free(img);
        return 0;
    }
    memcpy(img->planes[1], data + offset, plane_size);
    offset += plane_size;

    plane_size = (size_t)img->stride[2] * ((img->d_h + 1) / 2);
    if (offset + plane_size > size) {
        vpx_img_free(img);
        return 0;
    }
    memcpy(img->planes[2], data + offset, plane_size);
    offset += plane_size;

    // Initialize encoder
    vpx_codec_ctx_t codec;
    vpx_codec_iface_t *iface = vpx_codec_vp8_cx();
    vpx_codec_enc_cfg_t cfg;
    if (vpx_codec_enc_config_default(iface, &cfg, 0) != VPX_CODEC_OK) {
        vpx_img_free(img);
        return 0;
    }

    cfg.g_w = width;
    cfg.g_h = height;
    cfg.g_bit_depth = bit_depth;
    cfg.g_input_bit_depth = bit_depth;
    cfg.g_timebase.num = 1;
    cfg.g_timebase.den = 30;
    cfg.rc_target_bitrate = 256;

    if (vpx_codec_enc_init(&codec, iface, &cfg, 0) != VPX_CODEC_OK) {
        vpx_img_free(img);
        return 0;
    }

    // Encode one frame
    vpx_codec_err_t res = vpx_codec_encode(&codec, img, 0, 1, 0, VPX_DL_REALTIME);
    if (res == VPX_CODEC_OK) {
        // Consume packets
        const vpx_codec_cx_pkt_t *pkt;
        vpx_codec_iter_t iter = NULL;
        while ((pkt = vpx_codec_get_cx_data(&codec, &iter)) != NULL) {
            // Packet data is consumed by reading it
            if (pkt->kind == VPX_CODEC_CX_FRAME_PKT) {
                volatile uint8_t sum = 0;
                const uint8_t *buf = (const uint8_t *)pkt->data.frame.buf;
                size_t sz = pkt->data.frame.sz;
                for (size_t i = 0; i < sz && i < 1024; i++) {
                    sum += buf[i];
                }
                (void)sum;
            }
        }
    }

    vpx_codec_destroy(&codec);
    vpx_img_free(img);
    return 0;
}