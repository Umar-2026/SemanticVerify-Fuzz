#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include "vpx/vpx_encoder.h"
#include "vpx/vp8cx.h"

#define IMG_WIDTH 64
#define IMG_HEIGHT 64
#define MAX_PACKETS 16

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1) return 0;

    vpx_image_t *img = NULL;
    vpx_codec_ctx_t codec;
    vpx_codec_enc_cfg_t cfg;
    vpx_codec_err_t res;
    int packets = 0;

    // Initialize encoder configuration
    res = vpx_codec_enc_config_default(vpx_codec_vp8_cx(), &cfg, 0);
    if (res != VPX_CODEC_OK) return 0;

    cfg.g_w = IMG_WIDTH;
    cfg.g_h = IMG_HEIGHT;
    cfg.g_timebase.num = 1;
    cfg.g_timebase.den = 30;
    cfg.rc_target_bitrate = 256;

    // Allocate image
    img = vpx_img_alloc(NULL, VPX_IMG_FMT_I420, IMG_WIDTH, IMG_HEIGHT, 1);
    if (!img) return 0;

    // Fill image planes with fuzz data
    size_t offset = 0;
    for (int plane = 0; plane < 3; plane++) {
        int w = (plane == 0) ? IMG_WIDTH : IMG_WIDTH / 2;
        int h = (plane == 0) ? IMG_HEIGHT : IMG_HEIGHT / 2;
        for (int y = 0; y < h; y++) {
            uint8_t *row = img->planes[plane] + y * img->stride[plane];
            for (int x = 0; x < w; x++) {
                if (offset < size) {
                    row[x] = data[offset++];
                } else {
                    row[x] = 0;
                }
            }
        }
    }

    // Initialize encoder
    res = vpx_codec_enc_init(&codec, vpx_codec_vp8_cx(), &cfg, 0);
    if (res != VPX_CODEC_OK) {
        vpx_img_free(img);
        return 0;
    }

    // Encode the image
    res = vpx_codec_encode(&codec, img, 0, 1, 0, VPX_DL_REALTIME);
    if (res == VPX_CODEC_OK) {
        // Consume generated packets
        const vpx_codec_cx_pkt_t *pkt;
        while ((pkt = vpx_codec_get_cx_data(&codec, &res)) != NULL) {
            if (pkt->kind == VPX_CODEC_CX_FRAME_PKT) {
                packets++;
                if (packets >= MAX_PACKETS) break;
            }
        }
    }

    // Cleanup
    vpx_codec_destroy(&codec);
    vpx_img_free(img);
    return 0;
}