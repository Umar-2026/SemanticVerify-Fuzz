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
    return min + (int)(val % (uint32_t)(max - min + 1));
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 16) return 0;

    int width = get_bounded_int(&data, &size, 16, MAX_WIDTH);
    int height = get_bounded_int(&data, &size, 16, MAX_HEIGHT);
    int bit_depth = get_bounded_int(&data, &size, 8, 8); // only 8-bit supported for simplicity
    int cpu_used = get_bounded_int(&data, &size, 0, 8);
    int rc_end_usage = get_bounded_int(&data, &size, 0, 1); // 0 = VBR, 1 = CBR
    int g_pass = get_bounded_int(&data, &size, 0, 1); // 0 = one pass, 1 = first pass
    int keyframe_interval = get_bounded_int(&data, &size, 1, 300);
    int lag_in_frames = get_bounded_int(&data, &size, 0, 25);
    int error_resilient = get_bounded_int(&data, &size, 0, 1);
    int threads = get_bounded_int(&data, &size, 1, 8);

    // Limit image size to avoid excessive memory usage
    if ((uint64_t)width * height > 16 * 1024 * 1024) return 0;

    vpx_codec_iface_t *iface = vpx_codec_vp8_cx();
    if (!iface) return 0;

    vpx_codec_enc_cfg_t cfg;
    if (vpx_codec_enc_config_default(iface, &cfg, 0) != VPX_CODEC_OK)
        return 0;

    cfg.g_w = width;
    cfg.g_h = height;
    cfg.g_bit_depth = bit_depth;
    cfg.g_timebase.num = 1;
    cfg.g_timebase.den = 30;
    cfg.g_pass = g_pass;
    cfg.g_lag_in_frames = lag_in_frames;
    cfg.rc_end_usage = rc_end_usage;
    cfg.rc_target_bitrate = 256; // kbps
    cfg.kf_min_dist = 0;
    cfg.kf_max_dist = keyframe_interval;
    cfg.g_error_resilient = error_resilient;
    cfg.g_threads = threads;

    vpx_codec_ctx_t codec;
    if (vpx_codec_enc_init(&codec, iface, &cfg, 0) != VPX_CODEC_OK)
        return 0;

    vpx_codec_control(&codec, VP8E_SET_CPUUSED, cpu_used);

    // Allocate image buffer (I420)
    size_t img_size = (size_t)width * height * 3 / 2;
    if (img_size == 0 || img_size > MAX_IMAGE_SIZE) {
        vpx_codec_destroy(&codec);
        return 0;
    }

    uint8_t *img_buf = (uint8_t *)malloc(img_size);
    if (!img_buf) {
        vpx_codec_destroy(&codec);
        return 0;
    }

    // Fill image with fuzz data, but ensure enough bytes available
    size_t copy_len = size < img_size ? size : img_size;
    if (copy_len > 0)
        memcpy(img_buf, data, copy_len);
    // Zero-fill remaining
    if (img_size > copy_len)
        memset(img_buf + copy_len, 0, img_size - copy_len);

    vpx_image_t img;
    if (!vpx_img_wrap(&img, VPX_IMG_FMT_I420, width, height, 1, img_buf)) {
        free(img_buf);
        vpx_codec_destroy(&codec);
        return 0;
    }

    // Encode a few frames
    vpx_codec_iter_t iter = NULL;
    const vpx_codec_cx_pkt_t *pkt;
    int frames_to_encode = 3;
    for (int frame = 0; frame < frames_to_encode; frame++) {
        vpx_codec_err_t res = vpx_codec_encode(&codec, &img, frame, 1, 0, VPX_DL_REALTIME);
        if (res != VPX_CODEC_OK)
            break;
        while ((pkt = vpx_codec_get_cx_data(&codec, &iter)) != NULL) {
            // Consume packet, no action needed
        }
        iter = NULL;
    }

    vpx_img_free(&img);
    free(img_buf);
    vpx_codec_destroy(&codec);
    return 0;
}