#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

#include "vpx/vpx_encoder.h"
#include "vpx/vp8cx.h"
#include "vpx/vpx_image.h"

#define WIDTH 64
#define HEIGHT 64
#define MAX_PACKETS 16

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1) return 0;

    vpx_codec_ctx_t codec;
    vpx_codec_enc_cfg_t cfg;
    vpx_image_t *img = NULL;
    vpx_codec_iter_t iter = NULL;
    const vpx_codec_cx_pkt_t *pkt;
    int packet_count = 0;
    int ret;

    // Initialize configuration
    if (vpx_codec_enc_config_default(vpx_codec_vp8_cx(), &cfg, 0) != VPX_CODEC_OK) {
        return 0;
    }

    cfg.g_w = WIDTH;
    cfg.g_h = HEIGHT;
    cfg.g_timebase.num = 1;
    cfg.g_timebase.den = 30;
    cfg.rc_target_bitrate = 256;

    // Initialize encoder
    if (vpx_codec_enc_init(&codec, vpx_codec_vp8_cx(), &cfg, 0) != VPX_CODEC_OK) {
        return 0;
    }

    // Allocate image
    img = vpx_img_alloc(NULL, VPX_IMG_FMT_I420, WIDTH, HEIGHT, 1);
    if (!img) {
        vpx_codec_destroy(&codec);
        return 0;
    }

    // Fill image planes with fuzz data
    size_t offset = 0;
    size_t plane_size_y = img->stride[0] * HEIGHT;
    size_t plane_size_uv = img->stride[1] * (HEIGHT / 2);

    for (size_t i = 0; i < plane_size_y && offset < size; i++) {
        img->planes[0][i] = data[offset++];
    }
    for (size_t i = 0; i < plane_size_uv && offset < size; i++) {
        img->planes[1][i] = data[offset++];
    }
    for (size_t i = 0; i < plane_size_uv && offset < size; i++) {
        img->planes[2][i] = data[offset++];
    }

    // Encode a few frames
    for (int frame = 0; frame < 3; frame++) {
        ret = vpx_codec_encode(&codec, img, frame, 1, 0, VPX_DL_REALTIME);
        if (ret != VPX_CODEC_OK) {
            break;
        }

        // Consume packets
        iter = NULL;
        while ((pkt = vpx_codec_get_cx_data(&codec, &iter)) != NULL) {
            if (pkt->kind == VPX_CODEC_CX_FRAME_PKT) {
                packet_count++;
                if (packet_count >= MAX_PACKETS) {
                    break;
                }
            }
        }
        if (packet_count >= MAX_PACKETS) {
            break;
        }
    }

    // Cleanup
    vpx_img_free(img);
    vpx_codec_destroy(&codec);

    return 0;
}