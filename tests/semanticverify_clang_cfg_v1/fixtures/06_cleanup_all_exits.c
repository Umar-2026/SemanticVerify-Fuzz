#include "zlib.h"
int LLVMFuzzerTestOneInput(const unsigned char *data, unsigned long size) {
  (void)data;
  z_stream strm = {0};
  int rc = deflateInit(&strm, Z_DEFAULT_COMPRESSION);
  if (rc != Z_OK) return 0;
  if (size == 0) {
    (void)deflateEnd(&strm);
    return 0;
  }
  (void)deflate(&strm, Z_NO_FLUSH);
  (void)deflateEnd(&strm);
  return 0;
}
