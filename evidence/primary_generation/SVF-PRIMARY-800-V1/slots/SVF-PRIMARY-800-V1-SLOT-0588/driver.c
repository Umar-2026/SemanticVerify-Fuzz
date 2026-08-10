#include <stdint.h>
#include <stddef.h>
#include "vpx/vpx_decoder.h"
#include "vpx/vp8dx.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 16) return 0;

    vpx_codec_ctx_t codec;
    vpx_codec_dec_cfg_t cfg = {0, 0, 0};
    vpx_codec_iface_t *interface = vpx_codec_vp8_dx();

    if (vpx_codec_dec_init(&codec, interface, &cfg, 0) != VPX_CODEC_OK) {
        return 0;
    }

    vpx_codec_err_t res = vpx_codec_decode(&codec, data, size, NULL, 0);

    switch (res) {
        case VPX_CODEC_OK:
            {
                vpx_codec_iter_t iter = NULL;
                vpx_image_t *img;
                while ((img = vpx_codec_get_frame(&codec, &iter)) != NULL) {
                    (void)img;
                }
            }
            break;
        case VPX_CODEC_MEM_ERROR:
        case VPX_CODEC_ABI_MISMATCH:
        case VPX_CODEC_INCAPABLE:
        case VPX_CODEC_UNSUP_BITSTREAM:
        case VPX_CODEC_UNSUP_FEATURE:
        case VPX_CODEC_CORRUPT_FRAME:
        case VPX_CODEC_INVALID_PARAM:
        case VPX_CODEC_LIST_END:
        default:
            break;
    }

    vpx_codec_destroy(&codec);
    return 0;
}