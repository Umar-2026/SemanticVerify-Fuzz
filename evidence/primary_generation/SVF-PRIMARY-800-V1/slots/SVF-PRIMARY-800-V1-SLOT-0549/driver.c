#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <vpx/vpx_encoder.h>
#include <vpx/vp8cx.h>

#define WIDTH 64
#define HEIGHT 64
#define FRAME_SIZE (WIDTH * HEIGHT * 3 / 2)

static void generate_frame(vpx_image_t *img, unsigned int seed) {
    unsigned int x, y;
    unsigned char *plane;
    unsigned int stride;
    unsigned int val;

    plane = img->planes[0];
    stride = img->stride[0];
    for (y = 0; y < HEIGHT; y++) {
        for (x = 0; x < WIDTH; x++) {
            val = (seed + x * 3 + y * 5) & 0xff;
            plane[y * stride + x] = (unsigned char)val;
        }
    }

    plane = img->planes[1];
    stride = img->stride[1];
    for (y = 0; y < HEIGHT / 2; y++) {
        for (x = 0; x < WIDTH / 2; x++) {
            val = (seed + x * 7 + y * 11) & 0xff;
            plane[y * stride + x] = (unsigned char)val;
        }
    }

    plane = img->planes[2];
    stride = img->stride[2];
    for (y = 0; y < HEIGHT / 2; y++) {
        for (x = 0; x < WIDTH / 2; x++) {
            val = (seed + x * 13 + y * 17) & 0xff;
            plane[y * stride + x] = (unsigned char)val;
        }
    }
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    vpx_codec_ctx_t codec;
    vpx_codec_enc_cfg_t cfg;
    vpx_image_t *img1 = NULL;
    vpx_image_t *img2 = NULL;
    vpx_codec_iter_t iter = NULL;
    const vpx_codec_cx_pkt_t *pkt;
    unsigned int seed1, seed2;
    int ret;

    if (size < 8) {
        return 0;
    }

    seed1 = (unsigned int)data[0] | ((unsigned int)data[1] << 8) |
            ((unsigned int)data[2] << 16) | ((unsigned int)data[3] << 24);
    seed2 = (unsigned int)data[4] | ((unsigned int)data[5] << 8) |
            ((unsigned int)data[6] << 16) | ((unsigned int)data[7] << 24);

    vpx_codec_dec_cfg_t dec_cfg;
    memset(&dec_cfg, 0, sizeof(dec_cfg));
    dec_cfg.threads = 1;
    dec_cfg.w = WIDTH;
    dec_cfg.h = HEIGHT;

    ret = vpx_codec_enc_config_default(vpx_codec_vp8_cx(), &cfg, 0);
    if (ret != VPX_CODEC_OK) {
        return 0;
    }

    cfg.g_w = WIDTH;
    cfg.g_h = HEIGHT;
    cfg.g_timebase.num = 1;
    cfg.g_timebase.den = 30;
    cfg.rc_target_bitrate = 256;

    ret = vpx_codec_enc_init(&codec, vpx_codec_vp8_cx(), &cfg, 0);
    if (ret != VPX_CODEC_OK) {
        return 0;
    }

    img1 = vpx_img_alloc(NULL, VPX_IMG_FMT_I420, WIDTH, HEIGHT, 1);
    img2 = vpx_img_alloc(NULL, VPX_IMG_FMT_I420, WIDTH, HEIGHT, 1);
    if (!img1 || !img2) {
        vpx_img_free(img1);
        vpx_img_free(img2);
        vpx_codec_destroy(&codec);
        return 0;
    }

    generate_frame(img1, seed1);
    generate_frame(img2, seed2);

    ret = vpx_codec_encode(&codec, img1, 0, 1, 0, VPX_DL_REALTIME);
    if (ret != VPX_CODEC_OK) {
        vpx_img_free(img1);
        vpx_img_free(img2);
        vpx_codec_destroy(&codec);
        return 0;
    }

    iter = NULL;
    while ((pkt = vpx_codec_get_cx_data(&codec, &iter)) != NULL) {
        if (pkt->kind == VPX_CODEC_CX_FRAME_PKT) {
            /* consume packet */
        }
    }

    ret = vpx_codec_encode(&codec, img2, 1, 1, 0, VPX_DL_REALTIME);
    if (ret != VPX_CODEC_OK) {
        vpx_img_free(img1);
        vpx_img_free(img2);
        vpx_codec_destroy(&codec);
        return 0;
    }

    iter = NULL;
    while ((pkt = vpx_codec_get_cx_data(&codec, &iter)) != NULL) {
        if (pkt->kind == VPX_CODEC_CX_FRAME_PKT) {
            /* consume packet */
        }
    }

    vpx_img_free(img1);
    vpx_img_free(img2);
    vpx_codec_destroy(&codec);

    return 0;
}