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
    uint16_t photometric;

    if (!TIFFGetField(tif, TIFFTAG_IMAGEWIDTH, &width) ||
        !TIFFGetField(tif, TIFFTAG_IMAGELENGTH, &height) ||
        !TIFFGetField(tif, TIFFTAG_BITSPERSAMPLE, &bits_per_sample) ||
        !TIFFGetField(tif, TIFFTAG_SAMPLESPERPIXEL, &samples_per_pixel) ||
        !TIFFGetField(tif, TIFFTAG_PLANARCONFIG, &planar_config) ||
        !TIFFGetField(tif, TIFFTAG_PHOTOMETRIC, &photometric)) {
        TIFFClose(tif);
        return 0;
    }

    // Limit allocation size to avoid excessive memory usage
    if (width == 0 || height == 0 || width > 65536 || height > 65536) {
        TIFFClose(tif);
        return 0;
    }

    uint64_t scanline_size = TIFFScanlineSize(tif);
    if (scanline_size == 0 || scanline_size > 1024 * 1024) {
        TIFFClose(tif);
        return 0;
    }

    uint8_t *scanline_buf = (uint8_t *)malloc(scanline_size);
    if (!scanline_buf) {
        TIFFClose(tif);
        return 0;
    }

    // Read a few scanlines (up to 4) using TIFFReadScanline
    uint32_t rows_to_read = height < 4 ? height : 4;
    for (uint32_t row = 0; row < rows_to_read; row++) {
        if (TIFFReadScanline(tif, scanline_buf, row, 0) < 0) {
            break;
        }
    }

    free(scanline_buf);

    // Attempt to read strips using TIFFReadEncodedStrip
    // Determine strip size and count
    uint32_t strip_size = TIFFStripSize(tif);
    if (strip_size > 0 && strip_size <= 1024 * 1024) {
        uint8_t *strip_buf = (uint8_t *)malloc(strip_size);
        if (strip_buf) {
            tstrip_t num_strips = TIFFNumberOfStrips(tif);
            // Read up to 4 strips
            tstrip_t strips_to_read = num_strips < 4 ? num_strips : 4;
            for (tstrip_t s = 0; s < strips_to_read; s++) {
                tmsize_t bytes_read = TIFFReadEncodedStrip(tif, s, strip_buf, strip_size);
                if (bytes_read < 0) {
                    break;
                }
            }
            free(strip_buf);
        }
    }

    TIFFClose(tif);
    return 0;
}