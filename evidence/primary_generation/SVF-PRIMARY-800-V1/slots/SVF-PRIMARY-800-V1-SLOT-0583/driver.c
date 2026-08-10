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

    // Use first byte to decide a small variation in decode flags
    int flags = 0;
    if (data[0] & 0x01) flags |= VPX_CODEC_USE_FRAME_THREADING;
    if (data[0] & 0x02) flags |= VPX_CODEC_USE_ERROR_CONCEALMENT;

    // Decode the rest of the input
    const uint8_t *payload = data + 1;
    size_t payload_size = size - 1;

    res = vpx_codec_decode(&codec, payload, payload_size, NULL, flags);

    // Produce several functional outcomes based on returned codec status
    if (res == VPX_CODEC_OK) {
        vpx_codec_iter_t iter = NULL;
        vpx_image_t *img;
        while ((img = vpx_codec_get_frame(&codec, &iter)) != NULL) {
            // Touch the frame data to ensure it's valid
            if (img->d_w > 0 && img->d_h > 0 && img->planes[0]) {
                volatile uint8_t sum = 0;
                for (unsigned int y = 0; y < img->d_h && y < 16; y++) {
                    for (unsigned int x = 0; x < img->d_w && x < 16; x++) {
                        sum += img->planes[0][y * img->stride[0] + x];
                    }
                }
                (void)sum;
            }
        }
    } else if (res == VPX_CODEC_UNSUP_BITSTREAM) {
        // Unsupported bitstream: just return
    } else if (res == VPX_CODEC_MEM_ERROR) {
        // Memory error: just return
    } else if (res == VPX_CODEC_ABI_MISMATCH) {
        // ABI mismatch: just return
    } else if (res == VPX_CODEC_INCAPABLE) {
        // Incapable: just return
    } else if (res == VPX_CODEC_INVALID_PARAM) {
        // Invalid parameter: just return
    } else if (res == VPX_CODEC_CORRUPT_FRAME) {
        // Corrupt frame: just return
    } else if (res == VPX_CODEC_ERROR) {
        // Generic error: just return
    } else {
        // Unknown status: just return
    }

    vpx_codec_destroy(&codec);
    return 0;
}