#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include "vpx/vpx_encoder.h"
#include "vpx/vp8cx.h"
#include "vpx/vpx_image.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 4) return 0;

    // Extract width and height from input, clamp to reasonable values
    uint16_t width = (data[0] << 8) | data[1];
    uint16_t height = (data[2] << 8) | data[3];
    if (width == 0 || height == 0) return 0;
    if (width > 4096) width = 4096;
    if (height > 4096) height = 4096;

    // Remaining data used as image pixel data
    const uint8_t *pixel_data = data + 4;
    size_t pixel_size = size - 4;

    // Initialize codec context
    vpx_codec_ctx_t codec;
    vpx_codec_iface_t *iface = vpx_codec_vp8_cx();
    vpx_codec_enc_cfg_t cfg;
    if (vpx_codec_enc_config_default(iface, &cfg, 0) != VPX_CODEC_OK) return 0;

    cfg.g_w = width;
    cfg.g_h = height;
    cfg.g_timebase.num = 1;
    cfg.g_timebase.den = 30;
    cfg.rc_target_bitrate = 256;

    if (vpx_codec_enc_init(&codec, iface, &cfg, 0) != VPX_CODEC_OK) return 0;

    // Allocate image
    vpx_image_t *img = vpx_img_alloc(NULL, VPX_IMG_FMT_I420, width, height, 1);
    if (!img) {
        vpx_codec_destroy(&codec);
        return 0;
    }

    // Fill image planes with pixel data (or zeros if insufficient)
    size_t y_size = (size_t)width * height;
    size_t uv_size = y_size / 4;
    size_t needed = y_size + 2 * uv_size;
    if (pixel_size < needed) {
        // Zero-fill missing data
        memset(img->planes[0], 0, y_size);
        memset(img->planes[1], 0, uv_size);
        memset(img->planes[2], 0, uv_size);
        if (pixel_size > 0) {
            size_t copy = pixel_size < y_size ? pixel_size : y_size;
            memcpy(img->planes[0], pixel_data, copy);
            if (pixel_size > y_size) {
                size_t rem = pixel_size - y_size;
                size_t copy_u = rem < uv_size ? rem : uv_size;
                memcpy(img->planes[1], pixel_data + y_size, copy_u);
                if (rem > uv_size) {
                    size_t copy_v = (rem - uv_size) < uv_size ? (rem - uv_size) : uv_size;
                    memcpy(img->planes[2], pixel_data + y_size + uv_size, copy_v);
                }
            }
        }
    } else {
        memcpy(img->planes[0], pixel_data, y_size);
        memcpy(img->planes[1], pixel_data + y_size, uv_size);
        memcpy(img->planes[2], pixel_data + y_size + uv_size, uv_size);
    }

    // Encode frame
    vpx_codec_encode(&codec, img, 0, 1, 0, VPX_DL_REALTIME);

    // Cleanup
    vpx_img_free(img);
    vpx_codec_destroy(&codec);
    return 0;
}