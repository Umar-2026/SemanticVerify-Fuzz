#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include "vpx/vp8dx.h"
#include "vpx/vpx_decoder.h"
#include "vpx/vpx_image.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 4) {
        return 0;
    }

    vpx_codec_ctx_t codec;
    vpx_codec_dec_cfg_t cfg;
    memset(&cfg, 0, sizeof(cfg));

    // Use fuzz input to set decoder configuration parameters.
    cfg.threads = data[0] % 8;
    cfg.w = (data[1] << 8) | data[2];
    cfg.h = data[3];

    vpx_codec_iface_t *iface = vpx_codec_vp8_dx();
    if (!iface) {
        return 0;
    }

    vpx_codec_err_t res = vpx_codec_dec_init(&codec, iface, &cfg, 0);
    if (res != VPX_CODEC_OK) {
        return 0;
    }

    // Process the remaining data as encoded input.
    if (size > 4) {
        vpx_codec_decode(&codec, data + 4, size - 4, NULL, 0);
    }

    vpx_codec_destroy(&codec);
    return 0;
}