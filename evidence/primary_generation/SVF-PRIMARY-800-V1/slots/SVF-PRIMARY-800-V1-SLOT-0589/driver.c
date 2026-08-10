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
    cfg.w = 0;
    cfg.h = 0;

    if (vpx_codec_dec_init(&codec, vpx_codec_vp8_dx(), &cfg, 0) != VPX_CODEC_OK) {
        return 0;
    }

    // Use first byte to decide a simple functional variation
    uint8_t variation = data[0];
    const uint8_t *payload = data + 1;
    size_t payload_size = size - 1;

    vpx_codec_err_t res;
    if (variation % 3 == 0) {
        res = vpx_codec_decode(&codec, payload, payload_size, NULL, 0);
    } else if (variation % 3 == 1) {
        res = vpx_codec_decode(&codec, payload, payload_size, NULL, VPX_DECODER_ABI_VERSION);
    } else {
        res = vpx_codec_decode(&codec, payload, payload_size, NULL, VPX_DECODER_ABI_VERSION | VPX_CODEC_USE_FRAME_THREADING);
    }

    if (res == VPX_CODEC_OK) {
        vpx_codec_iter_t iter = NULL;
        vpx_image_t *img;
        while ((img = vpx_codec_get_frame(&codec, &iter)) != NULL) {
            // Consume frame data to ensure it's processed
            volatile uint8_t sum = 0;
            for (unsigned int y = 0; y < img->d_h; y++) {
                for (unsigned int x = 0; x < img->d_w; x++) {
                    sum += img->planes[0][y * img->stride[0] + x];
                }
            }
            (void)sum;
        }
    } else if (res == VPX_CODEC_UNSUP_BITSTREAM) {
        // Handle unsupported bitstream case
        vpx_codec_err_t detail = vpx_codec_error(&codec);
        (void)detail;
    } else if (res == VPX_CODEC_MEM_ERROR) {
        // Handle memory error case
        vpx_codec_err_t detail = vpx_codec_error(&codec);
        (void)detail;
    } else {
        // Other error
        vpx_codec_err_t detail = vpx_codec_error(&codec);
        (void)detail;
    }

    vpx_codec_destroy(&codec);
    return 0;
}