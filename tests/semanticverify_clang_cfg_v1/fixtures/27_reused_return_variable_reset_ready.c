#include "zlib.h"

int main(void) {
    z_stream stream = {0};
    Bytef input[1] = {0};
    Bytef output[64];
    const Bytef dictionary[] = {'s', 'v', 'f'};

    int rc = deflateInit(
        &stream,
        Z_DEFAULT_COMPRESSION
    );
    if (rc != Z_OK)
        return 1;

    stream.next_in = input;
    stream.avail_in = sizeof(input);
    stream.next_out = output;
    stream.avail_out = sizeof(output);

    rc = deflate(&stream, Z_SYNC_FLUSH);
    if (rc != Z_OK) {
        deflateEnd(&stream);
        return 2;
    }

    rc = deflateReset(&stream);
    if (rc != Z_OK) {
        deflateEnd(&stream);
        return 3;
    }

    rc = deflateSetDictionary(
        &stream,
        dictionary,
        sizeof(dictionary)
    );
    if (rc != Z_OK) {
        deflateEnd(&stream);
        return 4;
    }

    rc = deflateEnd(&stream);
    if (rc != Z_OK)
        return 5;

    return 0;
}
