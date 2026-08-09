#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <tiffio.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 8) return 0;

    // Create a temporary file to hold the input data
    char filename[] = "/tmp/libtiff_fuzz_XXXXXX";
    int fd = mkstemp(filename);
    if (fd < 0) return 0;
    FILE *fp = fdopen(fd, "wb");
    if (!fp) {
        close(fd);
        unlink(filename);
        return 0;
    }
    fwrite(data, 1, size, fp);
    fclose(fp);

    TIFF *tif = TIFFOpen(filename, "r");
    unlink(filename);
    if (!tif) return 0;

    uint32_t width, height;
    uint16_t bits_per_sample, samples_per_pixel, planar_config;
    uint32_t rows_per_strip;

    TIFFGetField(tif, TIFFTAG_IMAGEWIDTH, &width);
    TIFFGetField(tif, TIFFTAG_IMAGELENGTH, &height);
    TIFFGetField(tif, TIFFTAG_BITSPERSAMPLE, &bits_per_sample);
    TIFFGetField(tif, TIFFTAG_SAMPLESPERPIXEL, &samples_per_pixel);
    TIFFGetField(tif, TIFFTAG_PLANARCONFIG, &planar_config);
    TIFFGetField(tif, TIFFTAG_ROWSPERSTRIP, &rows_per_strip);

    if (width == 0 || height == 0 || rows_per_strip == 0) {
        TIFFClose(tif);
        return 0;
    }

    // Compute scanline size in bytes
    tmsize_t scanline_size = TIFFScanlineSize(tif);
    if (scanline_size <= 0) {
        TIFFClose(tif);
        return 0;
    }

    // Allocate buffer for one scanline
    uint8_t *scanline_buf = (uint8_t *)malloc(scanline_size);
    if (!scanline_buf) {
        TIFFClose(tif);
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

    // Allocate buffer for one strip
    tmsize_t strip_size = TIFFStripSize(tif);
    if (strip_size > 0) {
        uint8_t *strip_buf = (uint8_t *)malloc(strip_size);
        if (strip_buf) {
            // Read a few strips (up to 4 or number of strips, whichever is smaller)
            tstrip_t num_strips = TIFFNumberOfStrips(tif);
            tstrip_t max_strips = num_strips < 4 ? num_strips : 4;
            for (tstrip_t strip = 0; strip < max_strips; strip++) {
                if (TIFFReadEncodedStrip(tif, strip, strip_buf, strip_size) < 0) {
                    break;
                }
            }
            free(strip_buf);
        }
    }

    TIFFClose(tif);
    return 0;
}