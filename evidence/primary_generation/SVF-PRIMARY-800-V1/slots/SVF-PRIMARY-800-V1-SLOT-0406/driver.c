#include <tiffio.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    char filename[256];
    snprintf(filename, sizeof(filename), "/tmp/fuzz_tiff_%d", getpid());

    FILE *fp = fopen(filename, "wb");
    if (!fp) {
        return 0;
    }
    fwrite(data, 1, size, fp);
    fclose(fp);

    TIFF *tif = TIFFOpen(filename, "r");
    if (tif) {
        uint32_t width = 0, height = 0;
        uint16_t samples = 0, bps = 0;

        TIFFGetField(tif, TIFFTAG_IMAGEWIDTH, &width);
        TIFFGetField(tif, TIFFTAG_IMAGELENGTH, &height);
        TIFFGetField(tif, TIFFTAG_SAMPLESPERPIXEL, &samples);
        TIFFGetField(tif, TIFFTAG_BITSPERSAMPLE, &bps);

        TIFFClose(tif);
    }

    unlink(filename);
    return 0;
}