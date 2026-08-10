#include <stdint.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "tiffio.h"

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
    if (!tif) {
        unlink(filename);
        return 0;
    }

    // Determine image dimensions and sample format
    uint32_t width, height;
    uint16_t bits_per_sample, samples_per_pixel;
    uint16_t planar_config;
    if (TIFFGetField(tif, TIFFTAG_IMAGEWIDTH, &width) &&
        TIFFGetField(tif, TIFFTAG_IMAGELENGTH, &height) &&
        TIFFGetField(tif, TIFFTAG_BITSPERSAMPLE, &bits_per_sample) &&
        TIFFGetField(tif, TIFFTAG_SAMPLESPERPIXEL, &samples_per_pixel) &&
        TIFFGetField(tif, TIFFTAG_PLANARCONFIG, &planar_config)) {
        // Compute scanline size in bytes
        tmsize_t scanline_size = TIFFScanlineSize(tif);
        if (scanline_size > 0 && scanline_size <= (tmsize_t)size) {
            uint8_t *buf = (uint8_t *)malloc((size_t)scanline_size);
            if (buf) {
                // Read a subset of scanlines based on input size
                uint32_t max_rows = (uint32_t)(size / (size_t)scanline_size);
                if (max_rows > height) max_rows = height;
                uint32_t rows_to_read = max_rows > 0 ? max_rows : 1;
                if (rows_to_read > height) rows_to_read = height;

                // Use first byte to decide starting row offset
                uint32_t start_row = data[0] % height;
                uint32_t rows_read = 0;
                for (uint32_t row = start_row; row < height && rows_read < rows_to_read; row++) {
                    if (TIFFReadScanline(tif, buf, row, 0) < 0) {
                        // Read failure: free and close
                        free(buf);
                        TIFFClose(tif);
                        unlink(filename);
                        return 0;
                    }
                    rows_read++;
                }

                // Functional outcome based on read results
                if (rows_read == rows_to_read) {
                    // Success: verify some bytes
                    uint32_t check_offset = data[1] % (uint32_t)scanline_size;
                    if (buf[check_offset] == data[2]) {
                        // Outcome A: data matches
                        free(buf);
                        TIFFClose(tif);
                        unlink(filename);
                        return 0;
                    } else {
                        // Outcome B: data differs
                        free(buf);
                        TIFFClose(tif);
                        unlink(filename);
                        return 0;
                    }
                } else {
                    // Outcome C: partial read
                    free(buf);
                    TIFFClose(tif);
                    unlink(filename);
                    return 0;
                }
            }
        }
    }

    TIFFClose(tif);
    unlink(filename);
    return 0;
}