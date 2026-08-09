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

    size_t scanline_size = TIFFScanlineSize(tif);
    uint8_t *buf = (uint8_t *)malloc(scanline_size);
    if (buf) {
        for (uint32_t row = 0; row < height; row++) {
            size_t offset = (row * scanline_size) % size;
            size_t copy_len = (scanline_size < (size - offset)) ? scanline_size : (size - offset);
            
            for (size_t i = 0; i < scanline_size; i++) {
                buf[i] = data[(offset + i) % size];
            }
            
            TIFFWriteScanline(tif, buf, row, 0);
        }
        free(buf);
    }

    TIFFClose(tif);
    return 0;
}