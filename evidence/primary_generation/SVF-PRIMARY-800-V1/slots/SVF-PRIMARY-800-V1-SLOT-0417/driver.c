#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include "tiffio.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 8) return 0;

    // Use first 4 bytes for width, next 4 for height
    uint32_t width = (uint32_t)data[0] | ((uint32_t)data[1] << 8) | ((uint32_t)data[2] << 16) | ((uint32_t)data[3] << 24);
    uint32_t height = (uint32_t)data[4] | ((uint32_t)data[5] << 8) | ((uint32_t)data[6] << 16) | ((uint32_t)data[7] << 24);

    // Limit dimensions to avoid excessive memory usage
    if (width == 0 || height == 0 || width > 1024 || height > 1024) return 0;

    // Remaining bytes for field values
    const uint8_t *field_data = data + 8;
    size_t field_size = size - 8;

    // Open output TIFF in memory (use a temp file)
    char filename[] = "/tmp/libtiff_fuzz_XXXXXX";
    int fd = mkstemp(filename);
    if (fd < 0) return 0;
    close(fd);

    TIFF *tif = TIFFOpen(filename, "w");
    if (!tif) {
        unlink(filename);
        return 0;
    }

    // Set basic fields
    TIFFSetField(tif, TIFFTAG_IMAGEWIDTH, width);
    TIFFSetField(tif, TIFFTAG_IMAGELENGTH, height);
    TIFFSetField(tif, TIFFTAG_BITSPERSAMPLE, 8);
    TIFFSetField(tif, TIFFTAG_SAMPLESPERPIXEL, 1);
    TIFFSetField(tif, TIFFTAG_ROWSPERSTRIP, TIFFDefaultStripSize(tif, width));
    TIFFSetField(tif, TIFFTAG_ORIENTATION, ORIENTATION_TOPLEFT);
    TIFFSetField(tif, TIFFTAG_PLANARCONFIG, PLANARCONFIG_CONTIG);
    TIFFSetField(tif, TIFFTAG_PHOTOMETRIC, PHOTOMETRIC_MINISBLACK);
    TIFFSetField(tif, TIFFTAG_COMPRESSION, COMPRESSION_NONE);
    TIFFSetField(tif, TIFFTAG_FILLORDER, FILLORDER_MSB2LSB);

    // Set a small fuzz-derived set of optional fields
    // Use field_data bytes to decide which fields to set and their values
    size_t offset = 0;
    if (field_size > 0) {
        uint8_t flags = field_data[0];
        offset = 1;
        if (flags & 0x01) {
            // Set software tag
            const char *software = "libtiff-fuzz";
            TIFFSetField(tif, TIFFTAG_SOFTWARE, software);
        }
        if (flags & 0x02) {
            // Set description tag
            const char *description = "fuzz-generated";
            TIFFSetField(tif, TIFFTAG_IMAGEDESCRIPTION, description);
        }
        if (flags & 0x04) {
            // Set resolution
            float xres = 72.0f, yres = 72.0f;
            if (offset + 8 <= field_size) {
                memcpy(&xres, field_data + offset, 4);
                memcpy(&yres, field_data + offset + 4, 4);
                offset += 8;
            }
            TIFFSetField(tif, TIFFTAG_XRESOLUTION, xres);
            TIFFSetField(tif, TIFFTAG_YRESOLUTION, yres);
            TIFFSetField(tif, TIFFTAG_RESOLUTIONUNIT, RESUNIT_INCH);
        }
        if (flags & 0x08) {
            // Set document name
            const char *docname = "fuzz.tif";
            TIFFSetField(tif, TIFFTAG_DOCUMENTNAME, docname);
        }
        if (flags & 0x10) {
            // Set artist
            const char *artist = "fuzzer";
            TIFFSetField(tif, TIFFTAG_ARTIST, artist);
        }
        if (flags & 0x20) {
            // Set datetime
            const char *datetime = "2024:01:01 00:00:00";
            TIFFSetField(tif, TIFFTAG_DATETIME, datetime);
        }
        if (flags & 0x40) {
            // Set host computer
            const char *host = "fuzz-host";
            TIFFSetField(tif, TIFFTAG_HOSTCOMPUTER, host);
        }
        if (flags & 0x80) {
            // Set make
            const char *make = "fuzz-make";
            TIFFSetField(tif, TIFFTAG_MAKE, make);
        }
    }

    // Write scanlines with simple pattern derived from input
    uint8_t *row = (uint8_t *)malloc(width);
    if (!row) {
        TIFFClose(tif);
        unlink(filename);
        return 0;
    }

    for (uint32_t y = 0; y < height; y++) {
        for (uint32_t x = 0; x < width; x++) {
            // Simple deterministic pattern
            row[x] = (uint8_t)((x + y) & 0xFF);
        }
        if (TIFFWriteScanline(tif, row, y, 0) < 0) {
            free(row);
            TIFFClose(tif);
            unlink(filename);
            return 0;
        }
    }

    free(row);
    TIFFClose(tif);
    unlink(filename);
    return 0;
}