#include <stdint.h>
#include <stddef.h>
#include "vpx/vpx_decoder.h"
#include "vpx/vp8dx.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < sizeof(vpx_codec_dec_cfg_t) + 1) {
        return 0;
    }

    vpx_codec_ctx_t codec;
    vpx_codec_dec_cfg_t cfg;
    
    memcpy(&cfg, data, sizeof(vpx_codec_dec_cfg_t));
    const uint8_t *payload = data + sizeof(vpx_codec_dec_cfg_t);
    size_t payload_size = size - sizeof(vpx_codec_dec_cfg_t);

    if (vpx_codec_dec_init(&codec, &vpx_codec_vp8_dx_algo, &cfg, 0) == VPX_CODEC_OK) {
        vpx_codec_decode(&codec, payload, (unsigned int)payload_size, NULL, 0);
        vpx_codec_destroy(&codec);
    }

    return 0;
}