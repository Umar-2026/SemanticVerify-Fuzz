#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include "vpx/vp8dx.h"
#include "vpx/vpx_decoder.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 4) {
        return 0;
    }

    vpx_codec_ctx_t codec;
    vpx_codec_dec_cfg_t cfg;
    memset(&cfg, 0, sizeof(cfg));

    // Derive decoder configuration from fuzz input.
    cfg.threads = data[0] % 8;
    cfg.w = (data[1] << 8) | data[2];
    cfg.h = data[3];

    // Use the rest of the input as encoded data.
    const uint8_t *encoded_data = data + 4;
    size_t encoded_size = size - 4;

    if (vpx_codec_dec_init(&codec, vpx_codec_vp8_dx(), &cfg, 0) != VPX_CODEC_OK) {
        return 0;
    }

    vpx_codec_decode(&codec, encoded_data, encoded_size, NULL, 0);

    vpx_codec_destroy(&codec);
    return 0;
}