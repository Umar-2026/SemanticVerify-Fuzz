#include "zlib.h"
int LLVMFuzzerTestOneInput(const unsigned char *data, unsigned long size) {
  (void)data; (void)size;
  z_stream strm = {0};
  int init_rc = deflateInit(&strm, Z_DEFAULT_COMPRESSION);
  if (init_rc != Z_OK) return 0;
  int deflate_rc = deflate(&strm, Z_FINISH);
  if (deflate_rc != Z_STREAM_END) {
    (void)deflateEnd(&strm);
    return 0;
  }
  (void)deflate(&strm, Z_FINISH);
  (void)deflateEnd(&strm);
  return 0;
}
