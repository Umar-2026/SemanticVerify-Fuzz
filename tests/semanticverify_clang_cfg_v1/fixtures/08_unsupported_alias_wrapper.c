#include "zlib.h"
static int wrapped_deflate(z_stream *stream) {
  return deflate(stream, Z_NO_FLUSH);
}
int LLVMFuzzerTestOneInput(const unsigned char *data, unsigned long size) {
  (void)data; (void)size;
  z_stream strm = {0};
  int rc = deflateInit(&strm, Z_DEFAULT_COMPRESSION);
  if (rc != Z_OK) return 0;
  z_stream *alias = &strm;
  (void)wrapped_deflate(alias);
  (void)deflateEnd(&strm);
  return 0;
}
