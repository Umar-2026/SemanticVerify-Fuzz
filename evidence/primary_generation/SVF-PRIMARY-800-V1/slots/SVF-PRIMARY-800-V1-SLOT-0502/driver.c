#include <stdint.h>
#include <stddef.h>
#include "vpx/vpx_decoder.h"
#include "vpx/vp8dx.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1) {
        return 0;
    }

    vpx_codec_ctx_t codec;
    vpx_codec_dec_cfg_t cfg = {0, 0, 0};
    vpx_codec_iface_t *interface = vpx_codec_vp8_dx();

    if (vpx_codec_dec_init(&codec, interface, &cfg, 0) != VPX_CODEC_OK) {
        return 0;
    }

    if (vpx_codec_decode(&codec, data, size, NULL, 0) == VPX_CODEC_OK) {
        vpx_codec_iter_t iter = NULL;
        vpx_image_t *img;
        while ((img = vpx_codec_get_frame(&codec, &iter)) != NULL) {
            // Frame successfully decoded, no further action needed for fuzzing
        }
    }

    vpx_codec_destroy(&codec);
    return 0;
}