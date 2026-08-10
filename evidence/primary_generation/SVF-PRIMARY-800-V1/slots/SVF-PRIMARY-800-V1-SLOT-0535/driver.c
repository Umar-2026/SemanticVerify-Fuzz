#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <stdlib.h>
#include "vpx/vp8dx.h"
#include "vpx/vpx_decoder.h"
#include "vpx/vpx_image.h"

#define CHUNK_SIZE 64
#define MAX_CHUNKS 128

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size == 0) {
        return 0;
    }

    vpx_codec_ctx_t codec;
    vpx_codec_dec_cfg_t cfg;
    memset(&cfg, 0, sizeof(cfg));
    cfg.threads = 1;
    cfg.w = 0;
    cfg.h = 0;

    if (vpx_codec_dec_init(&codec, vpx_codec_vp8_dx(), &cfg, 0) != VPX_CODEC_OK) {
        return 0;
    }

    size_t offset = 0;
    size_t chunk_index = 0;
    while (offset < size && chunk_index < MAX_CHUNKS) {
        size_t chunk_size = size - offset;
        if (chunk_size > CHUNK_SIZE) {
            chunk_size = CHUNK_SIZE;
        }

        if (vpx_codec_decode(&codec, data + offset, chunk_size, NULL, 0) != VPX_CODEC_OK) {
            break;
        }

        vpx_codec_iter_t iter = NULL;
        vpx_image_t *img;
        while ((img = vpx_codec_get_frame(&codec, &iter)) != NULL) {
            // Consume the frame data to ensure it's processed.
            if (img->d_w > 0 && img->d_h > 0) {
                // Touch the first pixel of each plane to force memory access.
                volatile uint8_t *p = img->planes[0];
                if (p != NULL) {
                    (void)*p;
                }
            }
        }

        offset += chunk_size;
        chunk_index++;
    }

    vpx_codec_destroy(&codec);
    return 0;
}