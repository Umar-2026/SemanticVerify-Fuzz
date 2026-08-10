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

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    uint32_t width, height, bitrate, keyframe_interval;
    uint32_t cpu_used, threads, deadline;
    int ret;
    vpx_codec_ctx_t codec;
    vpx_codec_enc_cfg_t cfg;
    vpx_image_t img;
    uint8_t *image_buf = NULL;
    size_t image_size;
    const uint8_t *p = data;
    size_t remaining = size;

    if (!read_u32(&p, &remaining, &width)) return 0;
    if (!read_u32(&p, &remaining, &height)) return 0;
    if (!read_u32(&p, &remaining, &bitrate)) return 0;
    if (!read_u32(&p, &remaining, &keyframe_interval)) return 0;
    if (!read_u32(&p, &remaining, &cpu_used)) return 0;
    if (!read_u32(&p, &remaining, &threads)) return 0;
    if (!read_u32(&p, &remaining, &deadline)) return 0;

    width = width % MAX_WIDTH;
    height = height % MAX_HEIGHT;
    if (width == 0 || height == 0) return 0;
    bitrate = bitrate % 1000000;
    keyframe_interval = keyframe_interval % 1000;
    cpu_used = cpu_used % 16;
    threads = threads % 8;
    deadline = deadline % 1000;

    if (vpx_codec_enc_config_default(vpx_codec_vp8_cx(), &cfg, 0) != VPX_CODEC_OK)
        return 0;

    cfg.g_w = width;
    cfg.g_h = height;
    cfg.g_timebase.num = 1;
    cfg.g_timebase.den = 30;
    cfg.g_threads = threads;
    cfg.g_pass = VPX_RC_ONE_PASS;
    cfg.rc_target_bitrate = bitrate;
    cfg.rc_end_usage = VPX_VBR;
    cfg.kf_min_dist = 0;
    cfg.kf_max_dist = keyframe_interval;

    if (vpx_codec_enc_init(&codec, vpx_codec_vp8_cx(), &cfg, 0) != VPX_CODEC_OK)
        return 0;

    image_size = width * height * 3 / 2;
    if (image_size > MAX_IMAGE_SIZE) {
        vpx_codec_destroy(&codec);
        return 0;
    }

    image_buf = (uint8_t *)malloc(image_size);
    if (!image_buf) {
        vpx_codec_destroy(&codec);
        return 0;
    }

    if (remaining > 0) {
        size_t copy = remaining < image_size ? remaining : image_size;
        memcpy(image_buf, p, copy);
        if (copy < image_size)
            memset(image_buf + copy, 0, image_size - copy);
    } else {
        memset(image_buf, 0, image_size);
    }

    if (!vpx_img_wrap(&img, VPX_IMG_FMT_I420, width, height, 1, image_buf)) {
        free(image_buf);
        vpx_codec_destroy(&codec);
        return 0;
    }

    vpx_codec_control(&codec, VP8E_SET_CPUUSED, cpu_used);
    vpx_codec_control(&codec, VP8E_SET_TOKEN_PARTITIONS, 0);

    ret = vpx_codec_encode(&codec, &img, 0, 1, 0, deadline);
    if (ret == VPX_CODEC_OK) {
        const vpx_codec_cx_pkt_t *pkt;
        vpx_codec_iter_t iter = NULL;
        while ((pkt = vpx_codec_get_cx_data(&codec, &iter)) != NULL) {
            // consume packet
        }
    }

    vpx_img_free(&img);
    free(image_buf);
    vpx_codec_destroy(&codec);
    return 0;
}