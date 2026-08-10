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
    if (tif) {
        uint32_t width, height;
        uint16_t bits_per_sample, samples_per_pixel;
        uint16_t planar_config;

        TIFFGetField(tif, TIFFTAG_IMAGEWIDTH, &width);
        TIFFGetField(tif, TIFFTAG_IMAGELENGTH, &height);
        TIFFGetField(tif, TIFFTAG_BITSPERSAMPLE, &bits_per_sample);
        TIFFGetField(tif, TIFFTAG_SAMPLESPERPIXEL, &samples_per_pixel);
        TIFFGetField(tif, TIFFTAG_PLANARCONFIG, &planar_config);

        // Compute scanline size safely
        uint64_t scanline_size = TIFFScanlineSize(tif);
        if (scanline_size == 0 || scanline_size > 1024 * 1024 * 16) {
            TIFFClose(tif);
            unlink(filename);
            return 0;
        }

        uint8_t *buf = (uint8_t *)malloc(scanline_size);
        if (!buf) {
            TIFFClose(tif);
            unlink(filename);
            return 0;
        }

        // Attempt to read scanlines
        int read_result = 0;
        uint32_t rows_to_read = height;
        if (rows_to_read > 1000) rows_to_read = 1000; // bound work

        for (uint32_t row = 0; row < rows_to_read; row++) {
            int ret = TIFFReadScanline(tif, buf, row, 0);
            if (ret < 0) {
                read_result = -1;
                break;
            } else if (ret == 0) {
                read_result = 1;
            } else {
                read_result = 2;
            }
        }

        // Multiple functional outcomes based on open and read results
        if (read_result == -1) {
            // Read failed: do nothing special
        } else if (read_result == 1) {
            // Some rows read successfully, some not
            // Just touch the buffer to ensure it's used
            if (buf[0] == 0xAA) {
                // dummy branch
            }
        } else if (read_result == 2) {
            // All rows read successfully
            // Compute a simple checksum over the buffer
            uint32_t checksum = 0;
            for (uint32_t i = 0; i < scanline_size; i++) {
                checksum += buf[i];
            }
            if (checksum == 0xDEADBEEF) {
                // dummy branch
            }
        } else {
            // No rows read (height == 0)
            // Just close
        }

        free(buf);
        TIFFClose(tif);
    } else {
        // Open failed: nothing to do
    }

    unlink(filename);
    return 0;
}