#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <stdlib.h>
#include "tiffio.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 16) return 0;

    TIFF *tif = TIFFOpen("/tmp/fuzz_output.tif", "w");
    if (!tif) return 0;

    uint32_t width = (data[0] << 24) | (data[1] << 16) | (data[2] << 8) | data[3];
    uint32_t height = (data[4] << 24) | (data[5] << 16) | (data[6] << 8) | data[7];
    uint16_t bits_per_sample = (data[8] << 8) | data[9];
    uint16_t samples_per_pixel = (data[10] << 8) | data[11];
    uint16_t compression = (data[12] << 8) | data[13];
    uint16_t photometric = (data[14] << 8) | data[15];

    if (width == 0 || height == 0 || width > 4096 || height > 4096) {
        TIFFClose(tif);
        return 0;
    }
    if (bits_per_sample == 0 || bits_per_sample > 64) {
        TIFFClose(tif);
        return 0;
    }
    if (samples_per_pixel == 0 || samples_per_pixel > 4) {
        TIFFClose(tif);
        return 0;
    }

    TIFFSetField(tif, TIFFTAG_IMAGEWIDTH, width);
    TIFFSetField(tif, TIFFTAG_IMAGELENGTH, height);
    TIFFSetField(tif, TIFFTAG_BITSPERSAMPLE, bits_per_sample);
    TIFFSetField(tif, TIFFTAG_SAMPLESPERPIXEL, samples_per_pixel);
    TIFFSetField(tif, TIFFTAG_COMPRESSION, compression);
    TIFFSetField(tif, TIFFTAG_PHOTOMETRIC, photometric);
    TIFFSetField(tif, TIFFTAG_PLANARCONFIG, PLANARCONFIG_CONTIG);
    TIFFSetField(tif, TIFFTAG_ROWSPERSTRIP, 1);

    size_t scanline_size = (width * bits_per_sample * samples_per_pixel + 7) / 8;
    if (scanline_size == 0 || scanline_size > 65536) {
        TIFFClose(tif);
        return 0;
    }

    uint8_t *scanline = (uint8_t *)malloc(scanline_size);
    if (!scanline) {
        TIFFClose(tif);
        return 0;
    }

    for (uint32_t row = 0; row < height; row++) {
        memset(scanline, 0, scanline_size);
        if (size > 16) {
            size_t copy_len = scanline_size < (size - 16) ? scanline_size : (size - 16);
            memcpy(scanline, data + 16, copy_len);
        }
        if (TIFFWriteScanline(tif, scanline, row, 0) < 0) {
            free(scanline);
            TIFFClose(tif);
            return 0;
        }
    }

    free(scanline);
    TIFFClose(tif);
    return 0;
}