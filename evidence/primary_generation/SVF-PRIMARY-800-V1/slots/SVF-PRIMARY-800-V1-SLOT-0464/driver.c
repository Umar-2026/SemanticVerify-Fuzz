#include <tiffio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 4) {
        return 0;
    }

    size_t split = size / 2;
    const uint8_t *data1 = data;
    size_t size1 = split;
    const uint8_t *data2 = data + split;
    size_t size2 = size - split;

    char filename1[] = "/tmp/fuzz1.tiff";
    char filename2[] = "/tmp/fuzz2.tiff";

    FILE *f1 = fopen(filename1, "wb");
    if (!f1) return 0;
    fwrite(data1, 1, size1, f1);
    fclose(f1);

    FILE *f2 = fopen(filename2, "wb");
    if (!f2) return 0;
    fwrite(data2, 1, size2, f2);
    fclose(f2);

    TIFF *tif1 = TIFFOpen(filename1, "r");
    TIFF *tif2 = TIFFOpen(filename2, "r");

    if (tif1 && tif2) {
        uint32_t w1, h1, w2, h2;
        TIFFGetField(tif1, TIFFTAG_IMAGEWIDTH, &w1);
        TIFFGetField(tif1, TIFFTAG_IMAGELENGTH, &h1);
        TIFFGetField(tif2, TIFFTAG_IMAGEWIDTH, &w2);
        TIFFGetField(tif2, TIFFTAG_IMAGELENGTH, &h2);
    }

    if (tif1) TIFFClose(tif1);
    if (tif2) TIFFClose(tif2);

    remove(filename1);
    remove(filename2);

    return 0;
}