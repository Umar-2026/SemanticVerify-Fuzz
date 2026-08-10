#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include "vpx/vpx_encoder.h"
#include "vpx/vp8cx.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 8) return 0;

    // Parse dimensions from input
    unsigned int width = (data[0] << 8) | data[1];
    unsigned int height = (data[2] << 8) | data[3];
    if (width == 0 || height == 0 || width > 4096 || height > 4096) return 0;

    // Determine frame size and ensure we have enough data
    size_t frame_size = (size_t)width * height * 3 / 2; // YUV420
    if (size < 8 + frame_size) return 0;

    const uint8_t *frame_data = data + 8;

    // Allocate image
    vpx_image_t *img = vpx_img_alloc(NULL, VPX_IMG_FMT_I420, width, height, 1);
    if (!img) return 0;

    // Copy Y plane
    memcpy(img->planes[0], frame_data, width * height);
    // Copy U plane
    memcpy(img->planes[1], frame_data + width * height, width * height / 4);
    // Copy V plane
    memcpy(img->planes[2], frame_data + width * height + width * height / 4, width * height / 4);

    // Initialize encoder
    vpx_codec_ctx_t codec;
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

    if (vpx_codec_enc_init(&codec, vpx_codec_vp8_cx(), &cfg, 0) != VPX_CODEC_OK) {
        vpx_img_free(img);
        return 0;
    }

    // Encode one frame
    vpx_codec_encode(&codec, img, 0, 1, 0, VPX_DL_REALTIME);

    // Consume packets
    vpx_codec_iter_t iter = NULL;
    const vpx_codec_cx_pkt_t *pkt;
    while ((pkt = vpx_codec_get_cx_data(&codec, &iter)) != NULL) {
        // Just consume the packet data
        if (pkt->kind == VPX_CODEC_CX_FRAME_PKT) {
            // pkt->data.frame.buf is available
        }
    }

    // Cleanup
    vpx_codec_destroy(&codec);
    vpx_img_free(img);

    return 0;
}