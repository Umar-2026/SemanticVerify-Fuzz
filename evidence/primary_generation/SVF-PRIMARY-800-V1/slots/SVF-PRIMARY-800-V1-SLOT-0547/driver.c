#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <vpx/vpx_encoder.h>
#include <vpx/vp8cx.h>

#define WIDTH 64
#define HEIGHT 64
#define FRAME_SIZE (WIDTH * HEIGHT * 3 / 2)

static void fill_frame(vpx_image_t *img, unsigned char fill_value) {
    unsigned char *buf = img->planes[0];
    int i;
    for (i = 0; i < WIDTH * HEIGHT; i++) {
        buf[i] = fill_value;
    }
    buf = img->planes[1];
    for (i = 0; i < WIDTH * HEIGHT / 4; i++) {
        buf[i] = fill_value / 2;
    }
    buf = img->planes[2];
    for (i = 0; i < WIDTH * HEIGHT / 4; i++) {
        buf[i] = fill_value / 3;
    }
}

int LLVMFuzzerTestOneInput(const unsigned char *data, size_t size) {
    if (size < 2) return 0;

    vpx_codec_ctx_t codec;
    vpx_codec_enc_cfg_t cfg;
    vpx_image_t img1, img2;
    unsigned char *raw1 = NULL, *raw2 = NULL;
    int ret;
    unsigned char fill1 = data[0];
    unsigned char fill2 = data[1];

    vpx_codec_err_t res = vpx_codec_enc_config_default(vpx_codec_vp8_cx(), &cfg, 0);
    if (res != VPX_CODEC_OK) return 0;

    cfg.g_w = WIDTH;
    cfg.g_h = HEIGHT;
    cfg.g_timebase.num = 1;
    cfg.g_timebase.den = 30;
    cfg.g_pass = VPX_RC_ONE_PASS;
    cfg.g_lag_in_frames = 0;
    cfg.rc_end_usage = VPX_CBR;
    cfg.rc_target_bitrate = 256;

    res = vpx_codec_enc_init(&codec, vpx_codec_vp8_cx(), &cfg, 0);
    if (res != VPX_CODEC_OK) return 0;

    raw1 = (unsigned char *)malloc(FRAME_SIZE);
    raw2 = (unsigned char *)malloc(FRAME_SIZE);
    if (!raw1 || !raw2) {
        free(raw1);
        free(raw2);
        vpx_codec_destroy(&codec);
        return 0;
    }

    memset(raw1, fill1, FRAME_SIZE);
    memset(raw2, fill2, FRAME_SIZE);

    if (!vpx_img_wrap(&img1, VPX_IMG_FMT_I420, WIDTH, HEIGHT, 1, raw1)) {
        free(raw1);
        free(raw2);
        vpx_codec_destroy(&codec);
        return 0;
    }
    if (!vpx_img_wrap(&img2, VPX_IMG_FMT_I420, WIDTH, HEIGHT, 1, raw2)) {
        free(raw1);
        free(raw2);
        vpx_codec_destroy(&codec);
        return 0;
    }

    fill_frame(&img1, fill1);
    fill_frame(&img2, fill2);

    vpx_codec_err_t enc_res = vpx_codec_encode(&codec, &img1, 0, 1, 0, VPX_DL_REALTIME);
    if (enc_res == VPX_CODEC_OK) {
        const vpx_codec_cx_pkt_t *pkt;
        while ((pkt = vpx_codec_get_cx_data(&codec, &enc_res)) != NULL) {
            if (pkt->kind == VPX_CODEC_CX_FRAME_PKT) {
                // consume packet
            }
        }
    }

    enc_res = vpx_codec_encode(&codec, &img2, 1, 1, 0, VPX_DL_REALTIME);
    if (enc_res == VPX_CODEC_OK) {
        const vpx_codec_cx_pkt_t *pkt;
        while ((pkt = vpx_codec_get_cx_data(&codec, &enc_res)) != NULL) {
            if (pkt->kind == VPX_CODEC_CX_FRAME_PKT) {
                // consume packet
            }
        }
    }

    vpx_img_free(&img1);
    vpx_img_free(&img2);
    free(raw1);
    free(raw2);
    vpx_codec_destroy(&codec);
    return 0;
}