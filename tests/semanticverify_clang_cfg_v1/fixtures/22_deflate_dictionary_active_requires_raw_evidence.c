#include "zlib.h"

int LLVMFuzzerTestOneInput(
    const unsigned char *data,
    unsigned long size) {
  z_stream stream = {0};
  unsigned char output[64] = {0};
  unsigned char dictionary[] = {1, 2, 3, 4};

  int init_rc =
      deflateInit(&stream, Z_DEFAULT_COMPRESSION);
  if (init_rc != Z_OK) return 0;

  stream.next_in = (Bytef *)data;
  stream.avail_in = (uInt)size;
  stream.next_out = output;
  stream.avail_out = sizeof(output);

  int deflate_rc = deflate(&stream, Z_NO_FLUSH);
  if (deflate_rc == Z_STREAM_END) {
    (void)deflateEnd(&stream);
    return 0;
  }

  (void)deflateSetDictionary(
      &stream, dictionary, sizeof(dictionary));
  (void)deflateEnd(&stream);
  return 0;
}
