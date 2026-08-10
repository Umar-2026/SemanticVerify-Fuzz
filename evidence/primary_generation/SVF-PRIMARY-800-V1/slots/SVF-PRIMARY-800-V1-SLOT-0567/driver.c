#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include "vpx/vp8dx.h"
#include "vpx/vpx_decoder.h"

#define VPX_CODEC_DECODER_CTX 0

static int vpx_codec_dec_init_wrapper(vpx_codec_ctx_t *ctx, vpx_codec_iface_t *iface, vpx_codec_dec_cfg_t *cfg, unsigned long flags) {
    return vpx_codec_dec_init(ctx, iface, cfg, flags);
}

static int vpx_codec_decode_wrapper(vpx_codec_ctx_t *ctx, const uint8_t *data, size_t data_sz, void *user_priv, long deadline) {
    return vpx_codec_decode(ctx, data, data_sz, user_priv, deadline);
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) {
        return 0;
    }

    // Split input into two parts
    size_t split = (size_t)data[0] * 256 + data[1];
    if (split > size - 2) {
        split = size - 2;
    }
    const uint8_t *part1 = data + 2;
    size_t part1_size = split;
    const uint8_t *part2 = data + 2 + split;
    size_t part2_size = size - 2 - split;

    vpx_codec_ctx_t ctx1;
    vpx_codec_ctx_t ctx2;
    vpx_codec_dec_cfg_t cfg;
    memset(&cfg, 0, sizeof(cfg));
    cfg.threads = 1;

    if (vpx_codec_dec_init_wrapper(&ctx1, vpx_codec_vp8_dx(), &cfg, 0) != VPX_CODEC_OK) {
        return 0;
    }
    if (vpx_codec_dec_init_wrapper(&ctx2, vpx_codec_vp8_dx(), &cfg, 0) != VPX_CODEC_OK) {
        vpx_codec_destroy(&ctx1);
        return 0;
    }

    if (part1_size > 0) {
        vpx_codec_decode_wrapper(&ctx1, part1, part1_size, NULL, 0);
    }
    if (part2_size > 0) {
        vpx_codec_decode_wrapper(&ctx2, part2, part2_size, NULL, 0);
    }

    vpx_codec_destroy(&ctx1);
    vpx_codec_destroy(&ctx2);
    return 0;
}