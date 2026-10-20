#include "zlib.h"
int LLVMFuzzerTestOneInput(const unsigned char *data, unsigned long size) {
  (void)data; (void)size;
  z_stream strm = {0};
  int rc = inflateInit(&strm);
  if (rc != Z_OK) {
    (void)inflate(&strm, Z_NO_FLUSH);
    return 0;
  }
  (void)inflateEnd(&strm);
  return 0;
}
