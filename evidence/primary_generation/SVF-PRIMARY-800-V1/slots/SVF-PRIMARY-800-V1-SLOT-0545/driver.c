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
    unsigned char *buf = img->planes[0];
    unsigned int stride = img->stride[0];
    for (y = 0; y < HEIGHT; y++) {
        for (x = 0; x < WIDTH; x++) {
            buf[y * stride + x] = (unsigned char)((x * 3 + y * 5 + seed * 7) & 0xFF);
        }
    }
    // Fill chroma planes with constant values
    memset(img->planes[1], 128, img->stride[1] * ((HEIGHT + 1) / 2));
    memset(img->planes[2], 128, img->stride[2] * ((HEIGHT + 1) / 2));
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

    vpx_codec_ctx_t codec;
    vpx_codec_enc_cfg_t cfg;
    vpx_image_t *img1 = NULL;
    vpx_image_t *img2 = NULL;
    vpx_codec_iter_t iter = NULL;
    const vpx_codec_cx_pkt_t *pkt;
    int ret;

    // Initialize configuration
    if (vpx_codec_enc_config_default(vpx_codec_vp8_cx(), &cfg, 0) != VPX_CODEC_OK)
        return 0;

    cfg.g_w = WIDTH;
    cfg.g_h = HEIGHT;
    cfg.g_timebase.num = 1;
    cfg.g_timebase.den = 30;
    cfg.g_pass = VPX_RC_ONE_PASS;
    cfg.g_lag_in_frames = 0;
    cfg.rc_end_usage = VPX_CBR;
    cfg.rc_target_bitrate = 256;
    cfg.kf_mode = VPX_KF_AUTO;

    // Create encoder context
    if (vpx_codec_enc_init(&codec, vpx_codec_vp8_cx(), &cfg, 0) != VPX_CODEC_OK)
        return 0;

    // Allocate and initialize first image
    img1 = vpx_img_alloc(NULL, VPX_IMG_FMT_I420, WIDTH, HEIGHT, 1);
    if (!img1) {
        vpx_codec_destroy(&codec);
        return 0;
    }
    generate_frame(img1, data[0]);

    // Encode first frame
    ret = vpx_codec_encode(&codec, img1, 0, 1, 0, VPX_DL_REALTIME);
    if (ret != VPX_CODEC_OK) {
        vpx_img_free(img1);
        vpx_codec_destroy(&codec);
        return 0;
    }

    // Retrieve encoded data for first frame
    while ((pkt = vpx_codec_get_cx_data(&codec, &iter)) != NULL) {
        if (pkt->kind == VPX_CODEC_CX_FRAME_PKT) {
            // Process packet (not needed for this test)
        }
    }

    // Allocate and initialize second image independently
    img2 = vpx_img_alloc(NULL, VPX_IMG_FMT_I420, WIDTH, HEIGHT, 1);
    if (!img2) {
        vpx_img_free(img1);
        vpx_codec_destroy(&codec);
        return 0;
    }
    generate_frame(img2, data[1]);

    // Encode second frame
    ret = vpx_codec_encode(&codec, img2, 1, 1, 0, VPX_DL_REALTIME);
    if (ret != VPX_CODEC_OK) {
        vpx_img_free(img1);
        vpx_img_free(img2);
        vpx_codec_destroy(&codec);
        return 0;
    }

    // Retrieve encoded data for second frame
    iter = NULL;
    while ((pkt = vpx_codec_get_cx_data(&codec, &iter)) != NULL) {
        if (pkt->kind == VPX_CODEC_CX_FRAME_PKT) {
            // Process packet (not needed for this test)
        }
    }

    // Cleanup
    vpx_img_free(img1);
    vpx_img_free(img2);
    vpx_codec_destroy(&codec);

    return 0;
}