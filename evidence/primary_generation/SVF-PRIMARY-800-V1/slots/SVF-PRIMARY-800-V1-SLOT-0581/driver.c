#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include "vpx/vpx_decoder.h"
#include "vpx/vp8dx.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1) return 0;

    vpx_codec_ctx_t codec;
    vpx_codec_dec_cfg_t cfg;
    memset(&cfg, 0, sizeof(cfg));
    cfg.threads = 1;

    // Initialize decoder
    vpx_codec_err_t init_res = vpx_codec_dec_init(&codec, vpx_codec_vp8_dx(), &cfg, 0);
    if (init_res != VPX_CODEC_OK) {
        // Functional outcome: init failure
        return 0;
    }

    // Use first byte to vary decode parameters
    uint8_t param = data[0];
    const uint8_t *payload = data + 1;
    size_t payload_size = size - 1;

    // Decode with optional flags
    vpx_codec_err_t decode_res;
    if (param & 0x01) {
        decode_res = vpx_codec_decode(&codec, payload, payload_size, NULL, VPX_DECODER_FLAG_OUTPUT_ALL);
    } else {
        decode_res = vpx_codec_decode(&codec, payload, payload_size, NULL, 0);
    }

    // Functional outcomes based on decode result
    if (decode_res == VPX_CODEC_OK) {
        // Success: try to get frames
        vpx_codec_iter_t iter = NULL;
        vpx_image_t *img;
        while ((img = vpx_codec_get_frame(&codec, &iter)) != NULL) {
            // Consume frame data
            if (img->d_w && img->d_h) {
                volatile uint8_t sum = 0;
                for (unsigned int y = 0; y < img->d_h; y++) {
                    for (unsigned int x = 0; x < img->d_w; x++) {
                        sum += img->planes[0][y * img->stride[0] + x];
                    }
                }
                (void)sum;
            }
        }
    } else if (decode_res == VPX_CODEC_ERROR) {
        // Error outcome: do nothing
    } else if (decode_res == VPX_CODEC_MEM_ERROR) {
        // Memory error outcome
    } else if (decode_res == VPX_CODEC_UNSUP_BITSTREAM) {
        // Unsupported bitstream outcome
    } else if (decode_res == VPX_CODEC_UNSUP_FEATURE) {
        // Unsupported feature outcome
    } else if (decode_res == VPX_CODEC_CORRUPT_FRAME) {
        // Corrupt frame outcome
    } else if (decode_res == VPX_CODEC_INVALID_PARAM) {
        // Invalid parameter outcome
    } else {
        // Unknown status
    }

    vpx_codec_destroy(&codec);
    return 0;
}