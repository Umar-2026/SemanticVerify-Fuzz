#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <stdlib.h>
#include "vpx/vpx_encoder.h"
#include "vpx/vp8cx.h"

#define MAX_WIDTH 4096
#define MAX_HEIGHT 4096
#define MAX_IMAGE_SIZE (MAX_WIDTH * MAX_HEIGHT * 3 / 2)

static int read_u32(const uint8_t **data, size_t *size, uint32_t *out) {
    if (*size < 4) return 0;
    *out = ((uint32_t)(*data)[0]) | ((uint32_t)(*data)[1] << 8) |
           ((uint32_t)(*data)[2] << 16) | ((uint32_t)(*data)[3] << 24);
    *data += 4;
    *size -= 4;
    return 1;
}

static int read_u16(const uint8_t **data, size_t *size, uint16_t *out) {
    if (*size < 2) return 0;
    *out = (uint16_t)((*data)[0] | ((uint16_t)(*data)[1] << 8));
    *data += 2;
    *size -= 2;
    return 1;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    uint32_t width, height, bitrate, keyframe_interval;
    uint16_t cpu_used, threads, deadline_choice;
    int deadline;
    vpx_codec_ctx_t codec;
    vpx_codec_enc_cfg_t cfg;
    vpx_image_t *img = NULL;
    uint8_t *image_data = NULL;
    size_t image_size;
    int ret;
    const vpx_codec_iface_t *iface = vpx_codec_vp8_cx();

    if (size < 20) return 0;

    if (!read_u32(&data, &size, &width)) return 0;
    if (!read_u32(&data, &size, &height)) return 0;
    if (!read_u32(&data, &size, &bitrate)) return 0;
    if (!read_u32(&data, &size, &keyframe_interval)) return 0;
    if (!read_u16(&data, &size, &cpu_used)) return 0;
    if (!read_u16(&data, &size, &threads)) return 0;
    if (!read_u16(&data, &size, &deadline_choice)) return 0;

    if (width == 0 || height == 0 || width > MAX_WIDTH || height > MAX_HEIGHT) return 0;
    if (bitrate == 0 || bitrate > 100000000) return 0;
    if (keyframe_interval == 0 || keyframe_interval > 1000) return 0;
    if (cpu_used > 16) return 0;
    if (threads > 64) return 0;

    switch (deadline_choice % 3) {
        case 0: deadline = VPX_DL_REALTIME; break;
        case 1: deadline = VPX_DL_GOOD_QUALITY; break;
        default: deadline = VPX_DL_BEST_QUALITY; break;
    }

    if (vpx_codec_enc_config_default(iface, &cfg, 0) != VPX_CODEC_OK) return 0;

    cfg.g_w = width;
    cfg.g_h = height;
    cfg.g_timebase.num = 1;
    cfg.g_timebase.den = 30;
    cfg.g_threads = threads;
    cfg.g_pass = VPX_RC_ONE_PASS;
    cfg.g_lag_in_frames = 0;
    cfg.rc_target_bitrate = bitrate;
    cfg.rc_end_usage = VPX_CBR;
    cfg.kf_min_dist = 0;
    cfg.kf_max_dist = keyframe_interval;

    if (vpx_codec_enc_init(&codec, iface, &cfg, 0) != VPX_CODEC_OK) return 0;

    image_size = (size_t)width * height * 3 / 2;
    if (image_size > MAX_IMAGE_SIZE) {
        vpx_codec_destroy(&codec);
        return 0;
    }

    img = vpx_img_alloc(NULL, VPX_IMG_FMT_I420, width, height, 1);
    if (img == NULL) {
        vpx_codec_destroy(&codec);
        return 0;
    }

    image_data = (uint8_t *)malloc(image_size);
    if (image_data == NULL) {
        vpx_img_free(img);
        vpx_codec_destroy(&codec);
        return 0;
    }

    size_t copy_size = size < image_size ? size : image_size;
    memcpy(image_data, data, copy_size);
    if (copy_size < image_size) {
        memset(image_data + copy_size, 0, image_size - copy_size);
    }

    // Fill planes
    size_t y_size = (size_t)width * height;
    size_t uv_size = y_size / 4;
    memcpy(img->planes[0], image_data, y_size);
    memcpy(img->planes[1], image_data + y_size, uv_size);
    memcpy(img->planes[2], image_data + y_size + uv_size, uv_size);

    vpx_codec_err_t res = vpx_codec_encode(&codec, img, 0, 1, 0, deadline);
    if (res == VPX_CODEC_OK) {
        const vpx_codec_cx_pkt_t *pkt;
        vpx_codec_iter_t iter = NULL;
        while ((pkt = vpx_codec_get_cx_data(&codec, &iter)) != NULL) {
            // consume packet
        }
    }

    free(image_data);
    vpx_img_free(img);
    vpx_codec_destroy(&codec);
    return 0;
}