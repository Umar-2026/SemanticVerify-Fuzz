#include "zlib.h"
int LLVMFuzzerTestOneInput(const unsigned char *data, unsigned long size) {
  (void)data; (void)size;
  z_stream a = {0};
  z_stream b = {0};
  int rca = deflateInit(&a, Z_DEFAULT_COMPRESSION);
  if (rca != Z_OK) return 0;
  int rcb = deflateInit(&b, Z_DEFAULT_COMPRESSION);
  if (rcb != Z_OK) {
    (void)deflateEnd(&a);
    return 0;
  }
  (void)deflate(&a, Z_NO_FLUSH);
  (void)deflate(&b, Z_NO_FLUSH);
  (void)deflateEnd(&b);
  (void)deflateEnd(&a);
  return 0;
}
