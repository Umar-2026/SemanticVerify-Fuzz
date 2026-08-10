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
        tsize_t scanline_size;

        TIFFGetField(tif, TIFFTAG_IMAGEWIDTH, &width);
        TIFFGetField(tif, TIFFTAG_IMAGELENGTH, &height);
        TIFFGetField(tif, TIFFTAG_BITSPERSAMPLE, &bits_per_sample);
        TIFFGetField(tif, TIFFTAG_SAMPLESPERPIXEL, &samples_per_pixel);
        TIFFGetField(tif, TIFFTAG_PLANARCONFIG, &planar_config);

        scanline_size = TIFFScanlineSize(tif);
        if (scanline_size > 0 && width > 0 && height > 0) {
            uint8_t *buf = (uint8_t *)malloc(scanline_size);
            if (buf) {
                // Try reading scanlines from top to bottom
                for (uint32_t row = 0; row < height; row++) {
                    if (TIFFReadScanline(tif, buf, row, 0) < 0) {
                        // Read failure: free and close
                        free(buf);
                        TIFFClose(tif);
                        unlink(filename);
                        return 1; // outcome: read failure
                    }
                }
                free(buf);
                // Successful read of all scanlines
                TIFFClose(tif);
                unlink(filename);
                return 2; // outcome: full read success
            } else {
                TIFFClose(tif);
                unlink(filename);
                return 3; // outcome: allocation failure
            }
        } else {
            // Invalid dimensions or scanline size
            TIFFClose(tif);
            unlink(filename);
            return 4; // outcome: invalid geometry
        }
    } else {
        unlink(filename);
        return 5; // outcome: open failure
    }
}