#include "zlib.h"
int LLVMFuzzerTestOneInput(const unsigned char *data, unsigned long size) {
  (void)data; (void)size;
  z_stream strm = {0};
  (void)deflate(&strm, Z_NO_FLUSH);
  return 0;
}
