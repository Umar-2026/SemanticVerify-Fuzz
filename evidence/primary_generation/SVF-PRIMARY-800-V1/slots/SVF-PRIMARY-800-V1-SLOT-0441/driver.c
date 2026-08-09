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
    ssize_t written = write(fd, data, size);
    if (written != (ssize_t)size) {
        close(fd);
        unlink(filename);
        return 0;
    }
    close(fd);

    TIFF *tif = TIFFOpen(filename, "r");
    if (!tif) {
        unlink(filename);
        return 0;
    }

    // Process the first directory
    if (TIFFReadDirectory(tif) != 1) {
        TIFFClose(tif);
        unlink(filename);
        return 0;
    }

    // Read basic information from the first directory
    uint32_t width, height;
    uint16_t bits_per_sample, samples_per_pixel;
    uint16_t photometric;
    TIFFGetField(tif, TIFFTAG_IMAGEWIDTH, &width);
    TIFFGetField(tif, TIFFTAG_IMAGELENGTH, &height);
    TIFFGetField(tif, TIFFTAG_BITSPERSAMPLE, &bits_per_sample);
    TIFFGetField(tif, TIFFTAG_SAMPLESPERPIXEL, &samples_per_pixel);
    TIFFGetField(tif, TIFFTAG_PHOTOMETRIC, &photometric);

    // Allocate a buffer for the first image
    if (width > 0 && height > 0 && width <= 10000 && height <= 10000) {
        tmsize_t scanline_size = TIFFScanlineSize(tif);
        if (scanline_size > 0) {
            uint8_t *buf = (uint8_t *)malloc(scanline_size);
            if (buf) {
                for (uint32_t row = 0; row < height; row++) {
                    if (TIFFReadScanline(tif, buf, row, 0) < 0) {
                        break;
                    }
                }
                free(buf);
            }
        }
    }

    // Iterate through all remaining directories
    while (TIFFReadDirectory(tif) == 1) {
        uint32_t dir_width, dir_height;
        uint16_t dir_bits, dir_samples, dir_photometric;
        TIFFGetField(tif, TIFFTAG_IMAGEWIDTH, &dir_width);
        TIFFGetField(tif, TIFFTAG_IMAGELENGTH, &dir_height);
        TIFFGetField(tif, TIFFTAG_BITSPERSAMPLE, &dir_bits);
        TIFFGetField(tif, TIFFTAG_SAMPLESPERPIXEL, &dir_samples);
        TIFFGetField(tif, TIFFTAG_PHOTOMETRIC, &dir_photometric);

        // Read scanlines from this directory
        if (dir_width > 0 && dir_height > 0 && dir_width <= 10000 && dir_height <= 10000) {
            tmsize_t scanline_size = TIFFScanlineSize(tif);
            if (scanline_size > 0) {
                uint8_t *buf = (uint8_t *)malloc(scanline_size);
                if (buf) {
                    for (uint32_t row = 0; row < dir_height; row++) {
                        if (TIFFReadScanline(tif, buf, row, 0) < 0) {
                            break;
                        }
                    }
                    free(buf);
                }
            }
        }
    }

    TIFFClose(tif);
    unlink(filename);
    return 0;
}