#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include "vpx/vp8dx.h"
#include "vpx/vpx_decoder.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1) return 0;

    vpx_codec_ctx_t codec;
    vpx_codec_dec_cfg_t cfg;
    memset(&cfg, 0, sizeof(cfg));
    cfg.threads = 1;

    vpx_codec_iface_t *iface = vpx_codec_vp8_dx();
    if (!iface) return 0;

    vpx_codec_err_t res = vpx_codec_dec_init(&codec, iface, &cfg, 0);
    if (res != VPX_CODEC_OK) return 0;

    uint8_t *buf = (uint8_t *)data;
    size_t buf_size = size;

    // Use first byte to decide decode mode
    uint8_t mode = data[0];
    buf++;
    buf_size--;

    if (buf_size == 0) {
        vpx_codec_destroy(&codec);
        return 0;
    }

    vpx_codec_err_t decode_res;
    if (mode % 3 == 0) {
        decode_res = vpx_codec_decode(&codec, buf, buf_size, NULL, 0);
    } else if (mode % 3 == 1) {
        // Decode with a user-provided data pointer
        void *user_priv = (void *)(uintptr_t)(mode & 0x0F);
        decode_res = vpx_codec_decode(&codec, buf, buf_size, user_priv, 0);
    } else {
        // Decode with a non-zero deadline
        decode_res = vpx_codec_decode(&codec, buf, buf_size, NULL, 1);
    }

    if (decode_res == VPX_CODEC_OK) {
        vpx_codec_iter_t iter = NULL;
        vpx_image_t *img;
        while ((img = vpx_codec_get_frame(&codec, &iter)) != NULL) {
            // Consume frame data to ensure it's processed
            volatile uint8_t sum = 0;
            for (int plane = 0; plane < 3; plane++) {
                uint8_t *plane_data = img->planes[plane];
                int stride = img->stride[plane];
                int h = (plane == 0) ? img->d_h : (img->d_h + 1) / 2;
                for (int y = 0; y < h; y++) {
                    for (int x = 0; x < stride; x++) {
                        sum += plane_data[y * stride + x];
                    }
                }
            }
            (void)sum;
        }
    } else if (decode_res == VPX_CODEC_CORRUPT_FRAME) {
        // Corrupt frame: try to get any available frames
        vpx_codec_iter_t iter = NULL;
        vpx_image_t *img;
        while ((img = vpx_codec_get_frame(&codec, &iter)) != NULL) {
            // Just touch the frame
            volatile uint8_t val = img->planes[0][0];
            (void)val;
        }
    } else if (decode_res == VPX_CODEC_UNSUP_BITSTREAM) {
        // Unsupported bitstream: nothing to do
    } else if (decode_res == VPX_CODEC_MEM_ERROR) {
        // Memory error: nothing to do
    } else if (decode_res == VPX_CODEC_ABI_MISMATCH) {
        // ABI mismatch: nothing to do
    } else if (decode_res == VPX_CODEC_INCAPABLE) {
        // Incapable: nothing to do
    } else if (decode_res == VPX_CODEC_INVALID_PARAM) {
        // Invalid parameter: nothing to do
    } else if (decode_res == VPX_CODEC_ERROR) {
        // Generic error: nothing to do
    }

    vpx_codec_destroy(&codec);
    return 0;
}