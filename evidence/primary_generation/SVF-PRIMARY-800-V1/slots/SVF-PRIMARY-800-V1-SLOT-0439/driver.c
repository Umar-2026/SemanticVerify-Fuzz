#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <tiffio.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

    // Create a temporary file to hold the input data
    char filename[] = "/tmp/libtiff_fuzz_XXXXXX";
    int fd = mkstemp(filename);
    if (fd < 0) return 0;
    FILE *f = fdopen(fd, "wb");
    if (!f) {
        close(fd);
        unlink(filename);
        return 0;
    }
    fwrite(data, 1, size, f);
    fclose(f);

    TIFF *tif = TIFFOpen(filename, "r");
    if (!tif) {
        unlink(filename);
        return 0;
    }

    uint32_t width, height;
    uint16_t bits_per_sample, samples_per_pixel;
    uint16_t planar_config;
    uint32_t rows_per_strip;

    TIFFGetField(tif, TIFFTAG_IMAGEWIDTH, &width);
    TIFFGetField(tif, TIFFTAG_IMAGELENGTH, &height);
    TIFFGetField(tif, TIFFTAG_BITSPERSAMPLE, &bits_per_sample);
    TIFFGetField(tif, TIFFTAG_SAMPLESPERPIXEL, &samples_per_pixel);
    TIFFGetField(tif, TIFFTAG_PLANARCONFIG, &planar_config);
    TIFFGetField(tif, TIFFTAG_ROWSPERSTRIP, &rows_per_strip);

    if (width == 0 || height == 0 || samples_per_pixel == 0 || bits_per_sample == 0) {
        TIFFClose(tif);
        unlink(filename);
        return 0;
    }

    // Compute scanline size and allocate buffer
    tmsize_t scanline_size = TIFFScanlineSize(tif);
    if (scanline_size <= 0) {
        TIFFClose(tif);
        unlink(filename);
        return 0;
    }

    uint8_t *scanline_buf = (uint8_t *)malloc(scanline_size);
    if (!scanline_buf) {
        TIFFClose(tif);
        unlink(filename);
        return 0;
    }

    // Read a few scanlines (up to 4 or height, whichever is smaller)
    uint32_t num_scanlines = height < 4 ? height : 4;
    for (uint32_t row = 0; row < num_scanlines; row++) {
        if (TIFFReadScanline(tif, scanline_buf, row, 0) < 0) {
            break;
        }
    }

    free(scanline_buf);

    // Also attempt strip reading if strips are present
    if (rows_per_strip > 0) {
        tmsize_t strip_size = TIFFStripSize(tif);
        if (strip_size > 0) {
            uint8_t *strip_buf = (uint8_t *)malloc(strip_size);
            if (strip_buf) {
                uint32_t num_strips = TIFFNumberOfStrips(tif);
                uint32_t strips_to_read = num_strips < 2 ? num_strips : 2;
                for (uint32_t s = 0; s < strips_to_read; s++) {
                    if (TIFFReadEncodedStrip(tif, s, strip_buf, strip_size) < 0) {
                        break;
                    }
                }
                free(strip_buf);
            }
        }
    }

    TIFFClose(tif);
    unlink(filename);
    return 0;
}