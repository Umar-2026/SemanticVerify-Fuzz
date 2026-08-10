#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include "vpx/vpx_encoder.h"
#include "vpx/vp8cx.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  if (size < 128 * 128 * 3) return 0;

  vpx_codec_ctx_t codec;
  vpx_codec_enc_cfg_t cfg;
  vpx_image_t img1, img2;

  vpx_codec_enc_config_default(vpx_codec_vp8_cx(), &cfg, 0);
  cfg.g_w = 128;
  cfg.g_h = 128;

  if (vpx_codec_enc_init(&codec, vpx_codec_vp8_cx(), &cfg, 0)) {
    return 0;
  }

  vpx_img_alloc(&img1, VPX_IMG_FMT_I420, 128, 128, 1);
  vpx_img_alloc(&img2, VPX_IMG_FMT_I420, 128, 128, 1);

  memcpy(img1.planes[0], data, 128 * 128);
  memcpy(img2.planes[0], data + (128 * 128), 128 * 128);

  vpx_codec_encode(&codec, &img1, 0, 1, 0, VPX_DL_REALTIME);
  const vpx_codec_cx_pkt_t *pkt;
  vpx_codec_iter_t iter = NULL;
  while ((pkt = vpx_codec_get_cx_data(&codec, &iter)) != NULL);

  vpx_codec_encode(&codec, &img2, 1, 1, 0, VPX_DL_REALTIME);
  iter = NULL;
  while ((pkt = vpx_codec_get_cx_data(&codec, &iter)) != NULL);

  vpx_img_free(&img1);
  vpx_img_free(&img2);
  vpx_codec_destroy(&codec);

  return 0;
}