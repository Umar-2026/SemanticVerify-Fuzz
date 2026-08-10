#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include "vpx/vpx_encoder.h"
#include "vpx/vp8cx.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  if (size < 128 * 128 * 3) return 0;

  vpx_codec_ctx_t codec;
  vpx_codec_enc_cfg_t cfg;
  vpx_image_t raw;

  vpx_codec_enc_config_default(vpx_codec_vp8_cx(), &cfg, 0);
  cfg.g_w = 128;
  cfg.g_h = 128;
  cfg.g_timebase.num = 1;
  cfg.g_timebase.den = 30;

  if (vpx_codec_enc_init(&codec, vpx_codec_vp8_cx(), &cfg, 0)) {
    return 0;
  }

  if (!vpx_img_alloc(&raw, VPX_IMG_FMT_I420, 128, 128, 1)) {
    vpx_codec_destroy(&codec);
    return 0;
  }

  for (int i = 0; i < 2; ++i) {
    size_t offset = i * (128 * 128);
    if (offset + (128 * 128) > size) break;

    memcpy(raw.planes[0], data + offset, 128 * 128);
    memset(raw.planes[1], 128, 128 * 128 / 4);
    memset(raw.planes[2], 128, 128 * 128 / 4);

    if (vpx_codec_encode(&codec, &raw, i, 1, 0, VPX_DL_REALTIME) == VPX_CODEC_OK) {
      vpx_codec_iter_t iter = NULL;
      const vpx_codec_cx_pkt_t *pkt;
      while ((pkt = vpx_codec_get_cx_data(&codec, &iter)) != NULL) {
        (void)pkt;
      }
    }
  }

  vpx_img_free(&raw);
  vpx_codec_destroy(&codec);
  return 0;
}