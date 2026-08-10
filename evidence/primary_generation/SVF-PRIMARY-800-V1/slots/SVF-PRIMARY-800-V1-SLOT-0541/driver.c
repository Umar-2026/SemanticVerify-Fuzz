#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <vpx/vpx_encoder.h>
#include <vpx/vp8cx.h>

#define WIDTH 64
#define HEIGHT 64
#define BIT_DEPTH 8

static void generate_frame(vpx_image_t *img, unsigned int seed) {
    unsigned int x, y;
    unsigned int val = seed;
    for (y = 0; y < HEIGHT; y++) {
        for (x = 0; x < WIDTH; x++) {
            val = val * 1103515245 + 12345;
            img->planes[0][y * img->stride[0] + x] = (val >> 16) & 0xFF;
        }
    }
    for (y = 0; y < HEIGHT; y++) {
        for (x = 0; x < WIDTH; x++) {
            val = val * 1103515245 + 12345;
            img->planes[1][y * img->stride[1] + x] = (val >> 16) & 0xFF;
            img->planes[2][y * img->stride[2] + x] = (val >> 16) & 0xFF;
        }
    }
}

int main(int argc, char **argv) {
    (void)argc;
    (void)argv;

    vpx_codec_ctx_t codec;
    vpx_codec_enc_cfg_t cfg;
    vpx_image_t *img1 = NULL;
    vpx_image_t *img2 = NULL;
    vpx_codec_iter_t iter = NULL;
    const vpx_codec_cx_pkt_t *pkt;
    int ret;
    int frame_count = 0;

    // Initialize configuration
    ret = vpx_codec_enc_config_default(vpx_codec_vp8_cx(), &cfg, 0);
    if (ret != VPX_CODEC_OK) {
        fprintf(stderr, "Failed to get default config: %s\n", vpx_codec_err_to_string(ret));
        return 1;
    }

    cfg.g_w = WIDTH;
    cfg.g_h = HEIGHT;
    cfg.g_timebase.num = 1;
    cfg.g_timebase.den = 30;
    cfg.g_lag_in_frames = 0;
    cfg.rc_target_bitrate = 256;

    // Allocate images
    img1 = vpx_img_alloc(NULL, VPX_IMG_FMT_I420, WIDTH, HEIGHT, 1);
    img2 = vpx_img_alloc(NULL, VPX_IMG_FMT_I420, WIDTH, HEIGHT, 1);
    if (!img1 || !img2) {
        fprintf(stderr, "Failed to allocate images\n");
        vpx_img_free(img1);
        vpx_img_free(img2);
        return 1;
    }

    // Generate two independent frames
    generate_frame(img1, 0x12345678);
    generate_frame(img2, 0x9ABCDEF0);

    // Initialize encoder
    ret = vpx_codec_enc_init(&codec, vpx_codec_vp8_cx(), &cfg, 0);
    if (ret != VPX_CODEC_OK) {
        fprintf(stderr, "Failed to init encoder: %s\n", vpx_codec_err_to_string(ret));
        vpx_img_free(img1);
        vpx_img_free(img2);
        return 1;
    }

    // Encode first frame
    ret = vpx_codec_encode(&codec, img1, 0, 1, 0, VPX_DL_REALTIME);
    if (ret != VPX_CODEC_OK) {
        fprintf(stderr, "Failed to encode frame 1: %s\n", vpx_codec_err_to_string(ret));
        vpx_codec_destroy(&codec);
        vpx_img_free(img1);
        vpx_img_free(img2);
        return 1;
    }

    // Retrieve packets for first frame
    iter = NULL;
    while ((pkt = vpx_codec_get_cx_data(&codec, &iter)) != NULL) {
        if (pkt->kind == VPX_CODEC_CX_FRAME_PKT) {
            frame_count++;
        }
    }

    // Encode second frame
    ret = vpx_codec_encode(&codec, img2, 1, 1, 0, VPX_DL_REALTIME);
    if (ret != VPX_CODEC_OK) {
        fprintf(stderr, "Failed to encode frame 2: %s\n", vpx_codec_err_to_string(ret));
        vpx_codec_destroy(&codec);
        vpx_img_free(img1);
        vpx_img_free(img2);
        return 1;
    }

    // Retrieve packets for second frame
    iter = NULL;
    while ((pkt = vpx_codec_get_cx_data(&codec, &iter)) != NULL) {
        if (pkt->kind == VPX_CODEC_CX_FRAME_PKT) {
            frame_count++;
        }
    }

    // Flush encoder
    ret = vpx_codec_encode(&codec, NULL, 2, 1, 0, VPX_DL_REALTIME);
    if (ret != VPX_CODEC_OK) {
        fprintf(stderr, "Failed to flush encoder: %s\n", vpx_codec_err_to_string(ret));
        vpx_codec_destroy(&codec);
        vpx_img_free(img1);
        vpx_img_free(img2);
        return 1;
    }

    iter = NULL;
    while ((pkt = vpx_codec_get_cx_data(&codec, &iter)) != NULL) {
        if (pkt->kind == VPX_CODEC_CX_FRAME_PKT) {
            frame_count++;
        }
    }

    printf("Encoded %d frames successfully\n", frame_count);

    vpx_codec_destroy(&codec);
    vpx_img_free(img1);
    vpx_img_free(img2);
    return 0;
}