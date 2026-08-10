#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include "vpx/vp8dx.h"
#include "vpx/vpx_decoder.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1) {
        return 0;
    }

    vpx_codec_ctx_t codec;
    vpx_codec_dec_cfg_t cfg;
    memset(&cfg, 0, sizeof(cfg));
    cfg.threads = 1;

    vpx_codec_iface_t *iface = vpx_codec_vp8_dx();
    if (!iface) {
        return 0;
    }

    vpx_codec_err_t res = vpx_codec_dec_init(&codec, iface, &cfg, 0);
    if (res != VPX_CODEC_OK) {
        return 0;
    }

    // Use first byte to choose a functional outcome path
    uint8_t mode = data[0];
    const uint8_t *payload = data + 1;
    size_t payload_size = size - 1;

    if (mode % 3 == 0) {
        // Normal decode
        res = vpx_codec_decode(&codec, payload, payload_size, NULL, 0);
        if (res != VPX_CODEC_OK) {
            vpx_codec_destroy(&codec);
            return 0;
        }
    } else if (mode % 3 == 1) {
        // Decode with zero-size input
        res = vpx_codec_decode(&codec, payload, 0, NULL, 0);
        if (res != VPX_CODEC_OK) {
            vpx_codec_destroy(&codec);
            return 0;
        }
    } else {
        // Decode with user data pointer
        uint32_t user_priv = 0x12345678;
        res = vpx_codec_decode(&codec, payload, payload_size, &user_priv, 0);
        if (res != VPX_CODEC_OK) {
            vpx_codec_destroy(&codec);
            return 0;
        }
    }

    vpx_codec_iter_t iter = NULL;
    vpx_image_t *img;
    while ((img = vpx_codec_get_frame(&codec, &iter)) != NULL) {
        // Consume frame data to ensure it's processed
        if (img->d_w > 0 && img->d_h > 0) {
            volatile uint8_t sum = 0;
            for (unsigned int i = 0; i < img->d_h; i++) {
                const uint8_t *row = img->planes[0] + i * img->stride[0];
                for (unsigned int j = 0; j < img->d_w; j++) {
                    sum += row[j];
                }
            }
            (void)sum;
        }
    }

    vpx_codec_destroy(&codec);
    return 0;
}