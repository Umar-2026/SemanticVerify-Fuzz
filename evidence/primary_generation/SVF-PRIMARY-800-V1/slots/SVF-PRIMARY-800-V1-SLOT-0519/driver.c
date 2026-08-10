#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <stdlib.h>
#include "vpx/vpx_encoder.h"
#include "vpx/vp8cx.h"

#define MAX_WIDTH 4096
#define MAX_HEIGHT 4096
#define MAX_IMAGE_SIZE (MAX_WIDTH * MAX_HEIGHT * 3 / 2)

static int get_bounded_int(const uint8_t **data, size_t *size, int min, int max) {
    if (*size < 4) return min;
    uint32_t val;
    memcpy(&val, *data, 4);
    *data += 4;
    *size -= 4;
    if (max <= min) return min;
    return min + (val % (max - min + 1));
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 16) return 0;

    int width = get_bounded_int(&data, &size, 16, MAX_WIDTH);
    int height = get_bounded_int(&data, &size, 16, MAX_HEIGHT);
    int bit_depth = get_bounded_int(&data, &size, 8, 12);
    int cpu_used = get_bounded_int(&data, &size, -8, 8);
    int rc_end_usage = get_bounded_int(&data, &size, 0, 1);
    int g_pass = get_bounded_int(&data, &size, 0, 1);
    int kf_mode = get_bounded_int(&data, &size, 0, 2);
    int threads = get_bounded_int(&data, &size, 1, 8);
    int lag_in_frames = get_bounded_int(&data, &size, 0, 25);
    int error_resilient = get_bounded_int(&data, &size, 0, 1);
    int end_usage = get_bounded_int(&data, &size, 0, 1);
    int target_bitrate = get_bounded_int(&data, &size, 100, 10000);
    int keyint_min = get_bounded_int(&data, &size, 0, 100);
    int keyint_max = get_bounded_int(&data, &size, 1, 300);
    int rc_resize_mode = get_bounded_int(&data, &size, 0, 3);
    int rc_resize_allowed = get_bounded_int(&data, &size, 0, 1);

    size_t image_size = (size_t)width * height * 3 / 2;
    if (image_size > MAX_IMAGE_SIZE || image_size == 0) return 0;
    if (size < image_size) return 0;

    vpx_codec_iface_t *iface = vpx_codec_vp8_cx();
    if (!iface) return 0;

    vpx_codec_enc_cfg_t cfg;
    if (vpx_codec_enc_config_default(iface, &cfg, 0) != VPX_CODEC_OK) return 0;

    cfg.g_w = width;
    cfg.g_h = height;
    cfg.g_bit_depth = bit_depth;
    cfg.g_timebase.num = 1;
    cfg.g_timebase.den = 30;
    cfg.g_threads = threads;
    cfg.g_lag_in_frames = lag_in_frames;
    cfg.g_error_resilient = error_resilient;
    cfg.g_pass = g_pass;
    cfg.kf_mode = kf_mode;
    cfg.kf_min_dist = keyint_min;
    cfg.kf_max_dist = keyint_max;
    cfg.rc_end_usage = rc_end_usage;
    cfg.rc_target_bitrate = target_bitrate;
    cfg.rc_resize_mode = rc_resize_mode;
    cfg.rc_resize_allowed = rc_resize_allowed;
    cfg.rc_min_quantizer = 0;
    cfg.rc_max_quantizer = 63;

    vpx_codec_ctx_t codec;
    if (vpx_codec_enc_init(&codec, iface, &cfg, 0) != VPX_CODEC_OK) return 0;

    vpx_image_t img;
    if (!vpx_img_alloc(&img, VPX_IMG_FMT_I420, width, height, 1)) {
        vpx_codec_destroy(&codec);
        return 0;
    }

    // Fill image planes with fuzz data
    size_t y_size = (size_t)width * height;
    size_t uv_size = y_size / 4;
    memcpy(img.planes[VPX_PLANE_Y], data, y_size);
    data += y_size;
    memcpy(img.planes[VPX_PLANE_U], data, uv_size);
    data += uv_size;
    memcpy(img.planes[VPX_PLANE_V], data, uv_size);

    vpx_codec_err_t res = vpx_codec_encode(&codec, &img, 0, 1, 0, VPX_DL_REALTIME);
    if (res == VPX_CODEC_OK) {
        const vpx_codec_cx_pkt_t *pkt;
        vpx_codec_iter_t iter = NULL;
        while ((pkt = vpx_codec_get_cx_data(&codec, &iter)) != NULL) {
            // Consume packet data
            if (pkt->kind == VPX_CODEC_CX_FRAME_PKT) {
                volatile size_t sz = pkt->data.frame.sz;
                (void)sz;
            }
        }
    }

    vpx_img_free(&img);
    vpx_codec_destroy(&codec);
    return 0;
}