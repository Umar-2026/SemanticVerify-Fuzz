#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include "vpx/vp8dx.h"
#include "vpx/vpx_decoder.h"

#define DECODER_INTERFACE vpx_codec_vp8_dx()

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) {
        return 0;
    }

    // Split input into two parts
    size_t half = size / 2;
    const uint8_t *data1 = data;
    size_t size1 = half;
    const uint8_t *data2 = data + half;
    size_t size2 = size - half;

    vpx_codec_ctx_t ctx1;
    vpx_codec_ctx_t ctx2;

    // Initialize first decoder
    if (vpx_codec_dec_init(&ctx1, DECODER_INTERFACE, NULL, 0) != VPX_CODEC_OK) {
        return 0;
    }

    // Initialize second decoder
    if (vpx_codec_dec_init(&ctx2, DECODER_INTERFACE, NULL, 0) != VPX_CODEC_OK) {
        vpx_codec_destroy(&ctx1);
        return 0;
    }

    // Decode first part with first decoder
    vpx_codec_decode(&ctx1, data1, size1, NULL, 0);

    // Decode second part with second decoder
    vpx_codec_decode(&ctx2, data2, size2, NULL, 0);

    // Cleanup
    vpx_codec_destroy(&ctx1);
    vpx_codec_destroy(&ctx2);

    return 0;
}