#include "zlib.h"

int LLVMFuzzerTestOneInput(
    const unsigned char *data,
    unsigned long size) {
  (void)data;
  (void)size;

  z_stream stream = {0};
  unsigned char dictionary[] = {1, 2, 3, 4};

  (void)deflateSetDictionary(
      &stream, dictionary, sizeof(dictionary));
  return 0;
}
