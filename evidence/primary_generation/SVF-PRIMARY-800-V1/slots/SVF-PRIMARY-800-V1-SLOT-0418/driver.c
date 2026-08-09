#include <tiffio.h>
#include <stdint.h>
#include <stdlib.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 10) {
        return 0;
    }

    TIFF *tif = TIFFOpen("/dev/null", "w");
    if (!tif) {
        return 0;
    }

    uint32_t width = (data[0] << 8) | data[1];
    uint32_t height = (data[2] << 8) | data[3];
    uint16_t samples = (data[4] % 3) + 1;
    uint16_t bits = 8;

    if (width == 0 || height == 0) {
        TIFFClose(tif);
        return 0;
    }

    TIFFSetField(tif, TIFFTAG_IMAGEWIDTH, width);
    TIFFSetField(tif, TIFFTAG_IMAGELENGTH, height);
    TIFFSetField(tif, TIFFTAG_BITSPERSAMPLE, bits);
    TIFFSetField(tif, TIFFTAG_SAMPLESPERPIXEL, samples);
    TIFFSetField(tif, TIFFTAG_PLANARCONFIG, PLANARCONFIG_CONTIG);
    TIFFSetField(tif, TIFFTAG_PHOTOMETRIC, PHOTOMETRIC_RGB);

    size_t row_size = width * samples;
    uint8_t *buffer = (uint8_t *)malloc(row_size);
    if (buffer) {
        for (uint32_t y = 0; y < height; y++) {
            size_t offset = (y * 5) % (size - (row_size % (size + 1)));
            for (size_t i = 0; i < row_size; i++) {
                buffer[i] = data[(offset + i) % size];
            }
            TIFFWriteScanline(tif, buffer, y, 0);
        }
        free(buffer);
    }

    TIFFClose(tif);
    return 0;
}