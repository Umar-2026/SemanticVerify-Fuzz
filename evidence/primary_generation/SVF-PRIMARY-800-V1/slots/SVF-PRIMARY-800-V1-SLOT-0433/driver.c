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
    uint16_t compression, photometric;
    uint32_t rows_per_strip;

    TIFFGetField(tif, TIFFTAG_IMAGEWIDTH, &width);
    TIFFGetField(tif, TIFFTAG_IMAGELENGTH, &height);
    TIFFGetFieldDefaulted(tif, TIFFTAG_BITSPERSAMPLE, &bits_per_sample);
    TIFFGetFieldDefaulted(tif, TIFFTAG_SAMPLESPERPIXEL, &samples_per_pixel);
    TIFFGetFieldDefaulted(tif, TIFFTAG_PLANARCONFIG, &planar_config);
    TIFFGetFieldDefaulted(tif, TIFFTAG_COMPRESSION, &compression);
    TIFFGetFieldDefaulted(tif, TIFFTAG_PHOTOMETRIC, &photometric);
    TIFFGetFieldDefaulted(tif, TIFFTAG_ROWSPERSTRIP, &rows_per_strip);

    // Limit memory usage to avoid excessive allocation
    if (width == 0 || height == 0 || width > 10000 || height > 10000) {
        TIFFClose(tif);
        return 0;
    }
    if (bits_per_sample == 0 || bits_per_sample > 64 || samples_per_pixel == 0 || samples_per_pixel > 4) {
        TIFFClose(tif);
        return 0;
    }

    // Compute scanline size and strip size
    tmsize_t scanline_size = TIFFScanlineSize(tif);
    if (scanline_size <= 0 || scanline_size > (tmsize_t)(width * samples_per_pixel * (bits_per_sample / 8) + 16)) {
        TIFFClose(tif);
        return 0;
    }

    // Allocate buffer for one scanline
    uint8_t *scanline_buf = (uint8_t *)malloc(scanline_size);
    if (!scanline_buf) {
        TIFFClose(tif);
        return 0;
    }

    // Read a limited number of scanlines (up to 64) using TIFFReadScanline
    uint32_t max_rows = height < 64 ? height : 64;
    for (uint32_t row = 0; row < max_rows; row++) {
        if (TIFFReadScanline(tif, scanline_buf, row, 0) < 0) {
            break;
        }
    }

    free(scanline_buf);

    // Now attempt strip reading
    tmsize_t strip_size = TIFFStripSize(tif);
    if (strip_size > 0 && strip_size <= (tmsize_t)(rows_per_strip * scanline_size + 1024)) {
        uint8_t *strip_buf = (uint8_t *)malloc(strip_size);
        if (strip_buf) {
            // Read up to 16 strips
            uint32_t num_strips = TIFFNumberOfStrips(tif);
            uint32_t max_strips = num_strips < 16 ? num_strips : 16;
            for (uint32_t s = 0; s < max_strips; s++) {
                if (TIFFReadEncodedStrip(tif, s, strip_buf, strip_size) < 0) {
                    break;
                }
            }
            free(strip_buf);
        }
    }

    TIFFClose(tif);
    return 0;
}