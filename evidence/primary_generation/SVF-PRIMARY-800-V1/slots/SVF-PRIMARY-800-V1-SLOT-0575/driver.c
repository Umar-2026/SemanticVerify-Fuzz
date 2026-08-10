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

    vpx_image_t *img = vpx_img_alloc(NULL, VPX_IMG_FMT_I420, IMG_WIDTH, IMG_HEIGHT, 1);
    if (!img) return 0;

    // Fill image planes with fuzz data
    size_t offset = 0;
    for (int plane = 0; plane < 3; plane++) {
        int w = (plane == 0) ? IMG_WIDTH : IMG_WIDTH / 2;
        int h = (plane == 0) ? IMG_HEIGHT : IMG_HEIGHT / 2;
        size_t plane_size = (size_t)w * h;
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

    vpx_codec_enc_cfg_t cfg;
    if (vpx_codec_enc_config_default(vpx_codec_vp8_cx(), &cfg, 0) != VPX_CODEC_OK) {
        vpx_img_free(img);
        return 0;
    }
    cfg.g_w = IMG_WIDTH;
    cfg.g_h = IMG_HEIGHT;
    cfg.g_timebase.num = 1;
    cfg.g_timebase.den = 30;
    cfg.rc_target_bitrate = 256;

    vpx_codec_ctx_t codec;
    if (vpx_codec_enc_init(&codec, vpx_codec_vp8_cx(), &cfg, 0) != VPX_CODEC_OK) {
        vpx_img_free(img);
        return 0;
    }

    vpx_codec_err_t res = vpx_codec_encode(&codec, img, 0, 1, 0, VPX_DL_REALTIME);
    if (res == VPX_CODEC_OK) {
        const vpx_codec_cx_pkt_t *pkt;
        int packet_count = 0;
        while ((pkt = vpx_codec_get_cx_data(&codec, &res)) != NULL) {
            if (pkt->kind == VPX_CODEC_CX_FRAME_PKT) {
                // Consume packet data
                volatile uint8_t sum = 0;
                const uint8_t *payload = (const uint8_t *)pkt->data.frame.buf;
                for (size_t i = 0; i < pkt->data.frame.sz && i < 4096; i++) {
                    sum += payload[i];
                }
                (void)sum;
            }
            packet_count++;
            if (packet_count >= MAX_PACKETS) break;
        }
    }

    vpx_codec_destroy(&codec);
    vpx_img_free(img);
    return 0;
}