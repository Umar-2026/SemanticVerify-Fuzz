#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include "vpx/vp8dx.h"
#include "vpx/vpx_decoder.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    vpx_codec_ctx_t codec;
    vpx_codec_iface_t *iface = vpx_codec_vp8_dx();
    if (!iface) return 0;

    if (vpx_codec_dec_init(&codec, iface, NULL, 0) != VPX_CODEC_OK) {
        return 0;
    }

    // Submit the entire input as one encoded chunk.
    if (size > 0) {
        vpx_codec_decode(&codec, data, size, NULL, 0);
    }

    // Iterate over all decoded frames.
    vpx_codec_iter_t iter = NULL;
    vpx_image_t *img;
    while ((img = vpx_codec_get_frame(&codec, &iter)) != NULL) {
        // Consume the frame data to prevent optimization.
        volatile uint8_t sum = 0;
        for (int plane = 0; plane < 3; plane++) {
            if (img->planes[plane] && img->d_w > 0 && img->d_h > 0) {
                int stride = img->stride[plane];
                int h = (plane == 0) ? img->d_h : (img->d_h + 1) / 2;
                for (int y = 0; y < h; y++) {
                    const uint8_t *row = img->planes[plane] + y * stride;
                    for (int x = 0; x < img->d_w; x++) {
                        sum += row[x];
                    }
                }
            }
        }
        (void)sum;
    }

    vpx_codec_destroy(&codec);
    return 0;
}