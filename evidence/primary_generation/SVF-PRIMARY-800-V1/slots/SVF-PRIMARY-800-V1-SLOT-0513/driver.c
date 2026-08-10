#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <stdlib.h>
#include "vpx/vpx_encoder.h"
#include "vpx/vp8cx.h"

#define MAX_WIDTH 4096
#define MAX_HEIGHT 4096
#define MAX_IMAGE_SIZE (MAX_WIDTH * MAX_HEIGHT * 3 / 2)

static int get_bounded_int(const uint8_t *data, size_t size, size_t *offset, int min, int max) {
    if (*offset >= size) return min;
    int val = data[*offset];
    (*offset)++;
    if (val < min) return min;
    if (val > max) return max;
    return val;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    size_t offset = 0;
    int width = get_bounded_int(data, size, &offset, 16, MAX_WIDTH);
    int height = get_bounded_int(data, size, &offset, 16, MAX_HEIGHT);
    int bitrate = get_bounded_int(data, size, &offset, 100000, 10000000);
    int keyframe_interval = get_bounded_int(data, size, &offset, 1, 1000);
    int cpu_used = get_bounded_int(data, size, &offset, -8, 8);
    int error_resilient = get_bounded_int(data, size, &offset, 0, 1);
    int end_usage = get_bounded_int(data, size, &offset, 0, 1); // 0 = VBR, 1 = CBR

    vpx_codec_iface_t *iface = vpx_codec_vp8_cx();
    if (!iface) return 0;

    vpx_codec_enc_cfg_t cfg;
    if (vpx_codec_enc_config_default(iface, &cfg, 0) != VPX_CODEC_OK) {
        return 0;
    }

    cfg.g_w = width;
    cfg.g_h = height;
    cfg.g_timebase.num = 1;
    cfg.g_timebase.den = 30;
    cfg.g_threads = 1;
    cfg.g_pass = VPX_RC_ONE_PASS;
    cfg.g_lag_in_frames = 0;
    cfg.rc_end_usage = end_usage ? VPX_CBR : VPX_VBR;
    cfg.rc_target_bitrate = bitrate / 1000; // in kbps
    cfg.kf_min_dist = 0;
    cfg.kf_max_dist = keyframe_interval;
    cfg.rc_min_quantizer = 2;
    cfg.rc_max_quantizer = 56;
    cfg.g_error_resilient = error_resilient;

    vpx_codec_ctx_t enc;
    if (vpx_codec_enc_init(&enc, iface, &cfg, 0) != VPX_CODEC_OK) {
        return 0;
    }

    vpx_codec_control(&enc, VP8E_SET_CPUUSED, cpu_used);

    // Allocate image buffer (I420 format)
    size_t y_size = (size_t)width * height;
    size_t uv_size = y_size / 4;
    size_t img_size = y_size + 2 * uv_size;
    if (img_size > MAX_IMAGE_SIZE) {
        vpx_codec_destroy(&enc);
        return 0;
    }

    uint8_t *img_data = (uint8_t *)malloc(img_size);
    if (!img_data) {
        vpx_codec_destroy(&enc);
        return 0;
    }

    // Fill image data from fuzz input, cycling if needed
    for (size_t i = 0; i < img_size; i++) {
        img_data[i] = data[(offset + i) % size];
    }

    vpx_image_t img;
    if (!vpx_img_wrap(&img, VPX_IMG_FMT_I420, width, height, 1, img_data)) {
        free(img_data);
        vpx_codec_destroy(&enc);
        return 0;
    }

    // Encode a few frames
    int frames_to_encode = 3;
    for (int frame = 0; frame < frames_to_encode; frame++) {
        vpx_codec_err_t res = vpx_codec_encode(&enc, &img, frame, 1, 0, VPX_DL_REALTIME);
        if (res != VPX_CODEC_OK) {
            break;
        }

        const vpx_codec_cx_pkt_t *pkt;
        while ((pkt = vpx_codec_get_cx_data(&enc, NULL)) != NULL) {
            // Process packet (just consume)
            if (pkt->kind == VPX_CODEC_CX_FRAME_PKT) {
                // Packet data is available; nothing to do
            }
        }
    }

    vpx_img_free(&img);
    free(img_data);
    vpx_codec_destroy(&enc);
    return 0;
}