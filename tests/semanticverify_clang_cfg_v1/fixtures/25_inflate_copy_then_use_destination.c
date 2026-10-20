#include "zlib.h"
int LLVMFuzzerTestOneInput(const unsigned char *data,
                           unsigned long size) {
  z_stream source = {0};
  z_stream destination = {0};
  int source_rc = inflateInit(&source);
  if (source_rc != Z_OK) return 0;
  int copy_rc = inflateCopy(&destination, &source);
  if (copy_rc != Z_OK) {
    (void)inflateEnd(&source);
    return 0;
  }
  destination.next_in = (Bytef *)data;
  destination.avail_in = (uInt)size;
  (void)inflate(&destination, Z_NO_FLUSH);
  (void)inflateEnd(&destination);
  (void)inflateEnd(&source);
  return 0;
}
