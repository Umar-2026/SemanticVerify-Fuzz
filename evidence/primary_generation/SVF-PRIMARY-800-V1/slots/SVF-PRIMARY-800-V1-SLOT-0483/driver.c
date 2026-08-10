#include <stdint.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "tiffio.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 8) return 0;

    // Create a temporary file to hold the fuzz input
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

    TIFFGetField(tif, TIFFTAG_IMAGEWIDTH, &width);
    TIFFGetField(tif, TIFFTAG_IMAGELENGTH, &height);
    TIFFGetField(tif, TIFFTAG_BITSPERSAMPLE, &bits_per_sample);
    TIFFGetField(tif, TIFFTAG_SAMPLESPERPIXEL, &samples_per_pixel);
    TIFFGetField(tif, TIFFTAG_PLANARCONFIG, &planar_config);

    // Limit allocation size to avoid excessive memory usage
    if (width == 0 || height == 0 || width > 10000 || height > 10000) {
        TIFFClose(tif);
        unlink(filename);
        return 0;
    }

    uint64_t scanline_size = TIFFScanlineSize(tif);
    if (scanline_size == 0 || scanline_size > 1024 * 1024) {
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

    // Attempt to read scanlines and implement multiple functional outcomes
    int read_success = 0;
    int read_fail = 0;
    int partial_read = 0;

    for (uint32_t row = 0; row < height; row++) {
        memset(buf, 0, scanline_size);
        tmsize_t result = TIFFReadScanline(tif, buf, row, 0);
        if (result == 1) {
            read_success++;
            // Outcome 1: Process successful read (e.g., compute checksum)
            uint32_t checksum = 0;
            for (tmsize_t i = 0; i < scanline_size; i++) {
                checksum = (checksum * 31 + buf[i]) & 0xFFFFFFFF;
            }
            // Use checksum to avoid optimization
            if (checksum == 0xDEADBEEF) {
                // Dummy branch to keep outcome distinct
                read_success++;
            }
        } else if (result == 0) {
            read_fail++;
            // Outcome 2: Handle failed read (e.g., stop reading)
            break;
        } else {
            partial_read++;
            // Outcome 3: Handle partial read (e.g., continue but note)
            // In libtiff, TIFFReadScanline returns 1 on success, 0 on failure, -1 on error
            // We treat -1 as partial/error
            break;
        }
    }

    // Outcome 4: If no scanlines were read successfully, try reading with different row order
    if (read_success == 0 && height > 0) {
        // Attempt to read the last scanline
        memset(buf, 0, scanline_size);
        tmsize_t result = TIFFReadScanline(tif, buf, height - 1, 0);
        if (result == 1) {
            read_success++;
        }
    }

    // Outcome 5: If all reads failed, try reading with planar config 1 (contig) vs 2 (separate)
    if (read_success == 0 && read_fail > 0 && planar_config == 2) {
        // Try reading with sample 0 only (already done), but also try sample 1 if exists
        if (samples_per_pixel > 1) {
            memset(buf, 0, scanline_size);
            tmsize_t result = TIFFReadScanline(tif, buf, 0, 1);
            if (result == 1) {
                read_success++;
            }
        }
    }

    // Outcome 6: If still no success, attempt to read a scanline with a different buffer size
    if (read_success == 0 && scanline_size > 0) {
        uint8_t *small_buf = (uint8_t *)malloc(scanline_size / 2 + 1);
        if (small_buf) {
            memset(small_buf, 0, scanline_size / 2 + 1);
            tmsize_t result = TIFFReadScanline(tif, small_buf, 0, 0);
            if (result == 1) {
                read_success++;
            }
            free(small_buf);
        }
    }

    // Use the counters to influence control flow (avoid dead code elimination)
    volatile int total = read_success + read_fail + partial_read;
    if (total == 0) {
        // No reads attempted
        TIFFClose(tif);
        free(buf);
        unlink(filename);
        return 0;
    }

    free(buf);
    TIFFClose(tif);
    unlink(filename);
    return 0;
}