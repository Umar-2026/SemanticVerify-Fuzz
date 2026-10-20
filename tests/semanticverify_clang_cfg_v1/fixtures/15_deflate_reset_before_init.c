#include "zlib.h"
int LLVMFuzzerTestOneInput(const unsigned char *data, unsigned long size) {
  (void)data; (void)size;
  z_stream strm = {0};
  (void)deflateReset(&strm);
  return 0;
}
