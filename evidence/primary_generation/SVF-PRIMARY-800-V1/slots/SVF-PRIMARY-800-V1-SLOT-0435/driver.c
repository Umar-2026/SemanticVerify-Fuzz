#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <tiffio.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 8) return 0;

    // Create a temporary file to hold the input data
    char filename[] = "/tmp/libtiff_fuzz_XXXXXX";
    int fd = mkstemp(filename);
    if (fd < 0) return 0;
    ssize_t written = write(fd, data, size);
    if (written != (ssize_t)size) {
        close(fd);
        unlink(filename);
        return 0;
    }
    close(fd);

    TIFF *tif = TIFFOpen(filename, "r");
    unlink(filename);
    if (!tif) return 0;

    uint32_t width, height;
    uint16_t bits_per_sample, samples_per_pixel;
    uint16_t planar_config;
    uint32_t rows_per_strip;

    if (TIFFGetField(tif, TIFFTAG_IMAGEWIDTH, &width) != 1 ||
        TIFFGetField(tif, TIFFTAG_IMAGELENGTH, &height) != 1 ||
        TIFFGetField(tif, TIFFTAG_BITSPERSAMPLE, &bits_per_sample) != 1 ||
        TIFFGetField(tif, TIFFTAG_SAMPLESPERPIXEL, &samples_per_pixel) != 1 ||
        TIFFGetField(tif, TIFFTAG_PLANARCONFIG, &planar_config) != 1) {
        TIFFClose(tif);
        return 0;
    }

    if (width == 0 || height == 0 || bits_per_sample == 0 || samples_per_pixel == 0) {
        TIFFClose(tif);
        return 0;
    }

    // Compute scanline size in bytes, guard against overflow
    uint64_t scanline_size_64 = (uint64_t)width * bits_per_sample * samples_per_pixel / 8;
    if (scanline_size_64 > 1024 * 1024 * 64) { // limit to 64 MB per scanline
        TIFFClose(tif);
        return 0;
    }
    size_t scanline_size = (size_t)scanline_size_64;
    if (scanline_size == 0) {
        TIFFClose(tif);
        return 0;
    }

    // Allocate buffer for one scanline
    uint8_t *buf = (uint8_t *)malloc(scanline_size);
    if (!buf) {
        TIFFClose(tif);
        return 0;
    }

    // Read a few scanlines (up to 4) using TIFFReadScanline
    uint32_t num_scanlines = height < 4 ? height : 4;
    for (uint32_t row = 0; row < num_scanlines; row++) {
        if (TIFFReadScanline(tif, buf, row, 0) < 0) {
            break;
        }
    }

    // Also attempt to read strips using TIFFReadEncodedStrip
    if (TIFFGetField(tif, TIFFTAG_ROWSPERSTRIP, &rows_per_strip) != 1) {
        rows_per_strip = TIFFDefaultStripSize(tif, 0);
    }
    if (rows_per_strip == 0) {
        rows_per_strip = 1;
    }

    uint32_t num_strips = (height + rows_per_strip - 1) / rows_per_strip;
    if (num_strips > 0) {
        // Determine strip size (may be approximate)
        tmsize_t strip_size = TIFFStripSize(tif);
        if (strip_size > 0 && strip_size <= (tmsize_t)(64 * 1024 * 1024)) {
            uint8_t *strip_buf = (uint8_t *)malloc((size_t)strip_size);
            if (strip_buf) {
                // Read up to 4 strips
                uint32_t num_strips_to_read = num_strips < 4 ? num_strips : 4;
                for (uint32_t s = 0; s < num_strips_to_read; s++) {
                    tmsize_t n = TIFFReadEncodedStrip(tif, s, strip_buf, (tmsize_t)strip_size);
                    if (n < 0) {
                        break;
                    }
                }
                free(strip_buf);
            }
        }
    }

    free(buf);
    TIFFClose(tif);
    return 0;
}