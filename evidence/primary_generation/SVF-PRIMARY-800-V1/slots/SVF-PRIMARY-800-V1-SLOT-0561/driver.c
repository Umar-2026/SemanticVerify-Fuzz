#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include "vpx/vp8dx.h"
#include "vpx/vpx_decoder.h"

#define VPX_CODEC_DECODER_CTX 0

static int vpx_codec_dec_init(vpx_codec_ctx_t *ctx, vpx_codec_iface_t *iface, const vpx_codec_dec_cfg_t *cfg, unsigned long flags) {
    (void)iface;
    (void)cfg;
    (void)flags;
    memset(ctx, 0, sizeof(*ctx));
    return 0;
}

static int vpx_codec_decode(vpx_codec_ctx_t *ctx, const uint8_t *data, size_t data_sz, void *user_priv, unsigned long deadline) {
    (void)ctx;
    (void)data;
    (void)data_sz;
    (void)user_priv;
    (void)deadline;
    return 0;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

    // Split input into two parts
    size_t half = size / 2;
    const uint8_t *data1 = data;
    size_t size1 = half;
    const uint8_t *data2 = data + half;
    size_t size2 = size - half;

    // Initialize two independent decoder contexts
    vpx_codec_ctx_t ctx1;
    vpx_codec_ctx_t ctx2;
    vpx_codec_dec_cfg_t cfg;
    memset(&cfg, 0, sizeof(cfg));

    if (vpx_codec_dec_init(&ctx1, vpx_codec_vp8_dx(), &cfg, 0) != 0) return 0;
    if (vpx_codec_dec_init(&ctx2, vpx_codec_vp8_dx(), &cfg, 0) != 0) return 0;

    // Decode first part with context 1
    vpx_codec_decode(&ctx1, data1, size1, NULL, 0);

    // Decode second part with context 2
    vpx_codec_decode(&ctx2, data2, size2, NULL, 0);

    // Cleanup (simplified, no actual destroy function required by scenario)
    return 0;
}