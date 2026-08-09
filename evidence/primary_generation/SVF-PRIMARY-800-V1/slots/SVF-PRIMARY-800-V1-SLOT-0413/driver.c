#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <tiffio.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 8) return 0;

    // Use first 4 bytes for width, next 4 for height (small values)
    uint32_t width = (data[0] << 24) | (data[1] << 16) | (data[2] << 8) | data[3];
    uint32_t height = (data[4] << 24) | (data[5] << 16) | (data[6] << 8) | data[7];
    if (width == 0 || height == 0 || width > 1024 || height > 1024) return 0;

    // Remaining bytes for field values and scanline data
    const uint8_t *p = data + 8;
    size_t remaining = size - 8;

    // Use a few bytes to derive bits per sample, samples per pixel, photometric
    uint16_t bits_per_sample = 8;
    uint16_t samples_per_pixel = 1;
    uint16_t photometric = PHOTOMETRIC_MINISBLACK;
    if (remaining > 0) {
        bits_per_sample = (p[0] % 2) ? 8 : 16;
        if (remaining > 1) samples_per_pixel = (p[1] % 2) ? 1 : 3;
        if (remaining > 2) photometric = (p[2] % 3) ? PHOTOMETRIC_MINISBLACK : PHOTOMETRIC_RGB;
    }

    // Compute scanline size
    uint32_t scanline_size = width * samples_per_pixel * (bits_per_sample / 8);
    if (scanline_size == 0) return 0;

    // Create a temporary file
    char filename[] = "/tmp/libtiff_fuzz_XXXXXX";
    int fd = mkstemp(filename);
    if (fd < 0) return 0;
    close(fd);

    TIFF *tif = TIFFOpen(filename, "w");
    if (!tif) {
        unlink(filename);
        return 0;
    }

    // Set fields
    TIFFSetField(tif, TIFFTAG_IMAGEWIDTH, width);
    TIFFSetField(tif, TIFFTAG_IMAGELENGTH, height);
    TIFFSetField(tif, TIFFTAG_BITSPERSAMPLE, bits_per_sample);
    TIFFSetField(tif, TIFFTAG_SAMPLESPERPIXEL, samples_per_pixel);
    TIFFSetField(tif, TIFFTAG_ROWSPERSTRIP, TIFFDefaultStripSize(tif, 0));
    TIFFSetField(tif, TIFFTAG_PHOTOMETRIC, photometric);
    TIFFSetField(tif, TIFFTAG_PLANARCONFIG, PLANARCONFIG_CONTIG);
    TIFFSetField(tif, TIFFTAG_COMPRESSION, COMPRESSION_NONE);
    TIFFSetField(tif, TIFFTAG_ORIENTATION, ORIENTATION_TOPLEFT);

    // Write scanlines using fuzz data
    uint8_t *row = (uint8_t *)malloc(scanline_size);
    if (!row) {
        TIFFClose(tif);
        unlink(filename);
        return 0;
    }

    size_t offset = 0;
    for (uint32_t y = 0; y < height; y++) {
        for (uint32_t i = 0; i < scanline_size; i++) {
            if (offset < remaining) {
                row[i] = p[offset++];
            } else {
                row[i] = 0;
            }
        }
        if (TIFFWriteScanline(tif, row, y, 0) < 0) {
            break;
        }
    }

    free(row);
    TIFFClose(tif);
    unlink(filename);
    return 0;
}