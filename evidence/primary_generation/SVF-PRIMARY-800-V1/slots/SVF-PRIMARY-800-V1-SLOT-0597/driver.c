#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include "vpx/vpx_decoder.h"
#include "vpx/vp8dx.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1) {
        return 0;
    }

    vpx_codec_ctx_t codec;
    vpx_codec_dec_cfg_t cfg;
    memset(&cfg, 0, sizeof(cfg));
    cfg.threads = 1;

    if (vpx_codec_dec_init(&codec, vpx_codec_vp8_dx(), &cfg, 0) != VPX_CODEC_OK) {
        return 0;
    }

    // Use first byte to choose a decode option (e.g., flags)
    unsigned int flags = data[0] & 0x01;

    vpx_codec_decode(&codec, data + 1, size - 1, NULL, flags);

    vpx_codec_iter_t iter = NULL;
    vpx_image_t *img;
    while ((img = vpx_codec_get_frame(&codec, &iter)) != NULL) {
        // Iterate over decoded frames; no further processing needed
    }

    vpx_codec_destroy(&codec);
    return 0;
}