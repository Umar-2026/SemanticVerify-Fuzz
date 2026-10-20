#include "zlib.h"
int LLVMFuzzerTestOneInput(const unsigned char *data, unsigned long size) {
  (void)data; (void)size;
  z_stream strm = {0};
  int rc = deflateInit(&strm, Z_DEFAULT_COMPRESSION);
  if (rc != Z_OK) return 0;
  (void)deflateEnd(&strm);
  (void)deflate(&strm, Z_NO_FLUSH);
  return 0;
}
