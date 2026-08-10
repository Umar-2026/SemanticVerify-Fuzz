#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include "vpx/vp8dx.h"
#include "vpx/vpx_decoder.h"

#define VPX_CODEC_DECODER_CTX 0

static int vpx_codec_dec_init_wrapper(vpx_codec_ctx_t *ctx, vpx_codec_iface_t *iface, vpx_codec_dec_cfg_t *cfg, unsigned long flags) {
    return vpx_codec_dec_init(ctx, iface, cfg, flags);
}

static int vpx_codec_decode_wrapper(vpx_codec_ctx_t *ctx, const uint8_t *data, size_t data_sz, void *user_priv, unsigned long deadline) {
    return vpx_codec_decode(ctx, data, data_sz, user_priv, deadline);
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) {
        return 0;
    }

    // Split input into two parts
    size_t split = (size_t)data[0] * 257 % (size - 1) + 1; // ensure split >= 1 and < size
    const uint8_t *data1 = data + 1;
    size_t size1 = split;
    const uint8_t *data2 = data + 1 + split;
    size_t size2 = size - 1 - split;

    vpx_codec_ctx_t ctx1, ctx2;
    vpx_codec_dec_cfg_t cfg1, cfg2;
    memset(&cfg1, 0, sizeof(cfg1));
    memset(&cfg2, 0, sizeof(cfg2));
    cfg1.threads = 1;
    cfg2.threads = 1;

    // Initialize two independent decoder contexts
    if (vpx_codec_dec_init_wrapper(&ctx1, vpx_codec_vp8_dx(), &cfg1, 0) != VPX_CODEC_OK) {
        return 0;
    }
    if (vpx_codec_dec_init_wrapper(&ctx2, vpx_codec_vp8_dx(), &cfg2, 0) != VPX_CODEC_OK) {
        vpx_codec_destroy(&ctx1);
        return 0;
    }

    // Decode first part with ctx1
    if (size1 > 0) {
        vpx_codec_decode_wrapper(&ctx1, data1, size1, NULL, 0);
    }

    // Decode second part with ctx2
    if (size2 > 0) {
        vpx_codec_decode_wrapper(&ctx2, data2, size2, NULL, 0);
    }

    // Cleanup
    vpx_codec_destroy(&ctx1);
    vpx_codec_destroy(&ctx2);

    return 0;
}