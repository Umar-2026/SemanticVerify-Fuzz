#include "zlib.h"

int LLVMFuzzerTestOneInput(
    const unsigned char *data,
    unsigned long size) {
  (void)data;
  (void)size;

  z_stream stream = {0};
  unsigned char dictionary[] = {1, 2, 3, 4};

  int init_rc =
      deflateInit(&stream, Z_DEFAULT_COMPRESSION);
  if (init_rc != Z_OK) return 0;

  int dictionary_rc = deflateSetDictionary(
      &stream, dictionary, sizeof(dictionary));
  (void)dictionary_rc;

  (void)deflateEnd(&stream);
  return 0;
}
