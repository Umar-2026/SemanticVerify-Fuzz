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

    if (width == 0 || height == 0 || width > 10000 || height > 10000) {
        TIFFClose(tif);
        unlink(filename);
        return 0;
    }

    // Compute scanline size
    tmsize_t scanline_size = TIFFScanlineSize(tif);
    if (scanline_size <= 0) {
        TIFFClose(tif);
        unlink(filename);
        return 0;
    }

    // Allocate buffer for one scanline
    unsigned char *buf = (unsigned char *)malloc(scanline_size);
    if (!buf) {
        TIFFClose(tif);
        unlink(filename);
        return 0;
    }

    // Read scanlines based on planar configuration
    int read_ok = 0;
    if (planar_config == PLANARCONFIG_CONTIG) {
        for (uint32_t row = 0; row < height; row++) {
            if (TIFFReadScanline(tif, buf, row, 0) < 0) {
                read_ok = -1;
                break;
            }
        }
        if (read_ok == 0) read_ok = 1;
    } else if (planar_config == PLANARCONFIG_SEPARATE) {
        uint16_t num_planes = samples_per_pixel;
        if (num_planes == 0) num_planes = 1;
        for (uint16_t plane = 0; plane < num_planes; plane++) {
            for (uint32_t row = 0; row < height; row++) {
                if (TIFFReadScanline(tif, buf, row, plane) < 0) {
                    read_ok = -2;
                    break;
                }
            }
            if (read_ok != 0) break;
        }
        if (read_ok == 0) read_ok = 2;
    } else {
        read_ok = -3;
    }

    // Perform different functional outcomes based on read result
    if (read_ok == 1) {
        // Contiguous: compute simple checksum of first scanline
        uint32_t checksum = 0;
        for (tmsize_t i = 0; i < scanline_size; i++) {
            checksum = (checksum << 1) ^ buf[i];
        }
        // Use checksum to influence a dummy operation
        volatile uint32_t dummy = checksum;
        (void)dummy;
    } else if (read_ok == 2) {
        // Separate: count non-zero bytes in first scanline
        uint32_t nonzero = 0;
        for (tmsize_t i = 0; i < scanline_size; i++) {
            if (buf[i] != 0) nonzero++;
        }
        volatile uint32_t dummy = nonzero;
        (void)dummy;
    } else {
        // Read failed: attempt to read a single scanline at row 0 anyway
        if (TIFFReadScanline(tif, buf, 0, 0) >= 0) {
            volatile uint32_t dummy = buf[0];
            (void)dummy;
        }
    }

    free(buf);
    TIFFClose(tif);
    unlink(filename);
    return 0;
}