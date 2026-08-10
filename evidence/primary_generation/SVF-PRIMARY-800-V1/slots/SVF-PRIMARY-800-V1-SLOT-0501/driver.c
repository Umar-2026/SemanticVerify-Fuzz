#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include "vpx/vpx_decoder.h"
#include "vpx/vp8dx.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    vpx_codec_ctx_t codec;
    vpx_codec_iface_t *iface = vpx_codec_vp8_dx();
    if (!iface) {
        return 0;
    }

    vpx_codec_dec_cfg_t cfg;
    memset(&cfg, 0, sizeof(cfg));
    cfg.threads = 1;

    if (vpx_codec_dec_init(&codec, iface, &cfg, 0) != VPX_CODEC_OK) {
        return 0;
    }

    vpx_codec_decode(&codec, data, size, NULL, 0);

    vpx_codec_iter_t iter = NULL;
    vpx_image_t *img;
    while ((img = vpx_codec_get_frame(&codec, &iter)) != NULL) {
        // Process frame if needed
    }

    vpx_codec_destroy(&codec);
    return 0;
}