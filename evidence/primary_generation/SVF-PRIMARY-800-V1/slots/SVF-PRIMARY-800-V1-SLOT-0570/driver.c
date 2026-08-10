#include <stdint.h>
#include <stddef.h>
#include "vpx/vpx_decoder.h"
#include "vpx/vp8dx.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  if (size < 16) return 0;

  vpx_codec_ctx_t codec1, codec2;
  vpx_codec_iface_t *interface = vpx_codec_vp8_dx();
  vpx_codec_dec_cfg_t cfg = {0, 0, 0};

  if (vpx_codec_dec_init(&codec1, interface, &cfg, 0) != VPX_CODEC_OK) {
    return 0;
  }
  if (vpx_codec_dec_init(&codec2, interface, &cfg, 0) != VPX_CODEC_OK) {
    vpx_codec_destroy(&codec1);
    return 0;
  }

  size_t half_size = size / 2;
  const uint8_t *part1 = data;
  const uint8_t *part2 = data + half_size;
  size_t size1 = half_size;
  size_t size2 = size - half_size;

  vpx_codec_decode(&codec1, part1, size1, NULL, 0);
  vpx_codec_decode(&codec2, part2, size2, NULL, 0);

  vpx_codec_destroy(&codec1);
  vpx_codec_destroy(&codec2);

  return 0;
}