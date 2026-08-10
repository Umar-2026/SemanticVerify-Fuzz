#include <stdint.h>
#include <stddef.h>
#include "vpx/vpx_decoder.h"
#include "vpx/vp8dx.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 16) return 0;

    vpx_codec_ctx_t codec;
    vpx_codec_dec_cfg_t cfg = {0, 0, 0};
    
    if (vpx_codec_dec_init(&codec, &vpx_codec_vp8_dx_algo, &cfg, 0)) {
        return 0;
    }

    size_t split_point = size / 2;
    const uint8_t *chunk1 = data;
    size_t size1 = split_point;
    const uint8_t *chunk2 = data + split_point;
    size_t size2 = size - split_point;

    vpx_codec_decode(&codec, chunk1, size1, NULL, 0);
    vpx_codec_decode(&codec, chunk2, size2, NULL, 0);

    vpx_codec_iter_t iter = NULL;
    vpx_image_t *img;
    while ((img = vpx_codec_get_frame(&codec, &iter)) != NULL) {
        // Frame processed
    }

    vpx_codec_destroy(&codec);
    return 0;
}