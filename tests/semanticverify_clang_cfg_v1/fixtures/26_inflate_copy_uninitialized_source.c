#include "zlib.h"
int LLVMFuzzerTestOneInput(const unsigned char *data,
                           unsigned long size) {
  (void)data; (void)size;
  z_stream source = {0};
  z_stream destination = {0};
  int copy_rc = inflateCopy(&destination, &source);
  if (copy_rc == Z_OK) {
    (void)inflateEnd(&destination);
  }
  return 0;
}
