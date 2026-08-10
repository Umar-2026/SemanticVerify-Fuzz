#include <stdint.h>
#include <stdlib.h>
#include "vpx/vpx_encoder.h"
#include "vpx/vp8cx.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  if (size < 1024) return 0;

  vpx_codec_ctx_t codec;
  vpx_codec_enc_cfg_t cfg;
  vpx_image_t img;
  vpx_codec_err_t res;

  vpx_codec_enc_config_default(vpx_codec_vp8_cx(), &cfg, 0);
  cfg.g_w = 16;
  cfg.g_h = 16;

  if (vpx_codec_enc_init(&codec, vpx_codec_vp8_cx(), &cfg, 0)) {
    return 0;
  }

  if (!vpx_img_alloc(&img, VPX_IMG_FMT_I420, cfg.g_w, cfg.g_h, 1)) {
    vpx_codec_destroy(&codec);
    return 0;
  }

  size_t plane_size = cfg.g_w * cfg.g_h;
  if (size >= plane_size * 3 / 2) {
    for (int i = 0; i < 3; ++i) {
      size_t p_size = (i == 0) ? plane_size : plane_size / 4;
      size_t offset = (i == 0) ? 0 : (plane_size + (i - 1) * (plane_size / 4));
      for (size_t j = 0; j < p_size; ++j) {
        img.planes[i][j] = data[offset + j];
      }
    }

    vpx_codec_encode(&codec, &img, 0, 1, 0, VPX_DL_REALTIME);

    vpx_codec_iter_t iter = NULL;
    const vpx_codec_cx_pkt_t *pkt;
    while ((pkt = vpx_codec_get_cx_data(&codec, &iter)) != NULL) {
      (void)pkt;
    }
  }

  vpx_img_free(&img);
  vpx_codec_destroy(&codec);

  return 0;
}