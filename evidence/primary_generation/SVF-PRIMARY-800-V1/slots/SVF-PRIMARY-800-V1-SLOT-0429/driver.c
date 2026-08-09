#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <tiffio.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

    // Create a temporary file to hold the fuzz data
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
    if (tif) {
        uint32_t w = 0, h = 0;
        uint16_t spp = 0, bps = 0, fmt = 0;
        TIFFGetField(tif, TIFFTAG_IMAGEWIDTH, &w);
        TIFFGetField(tif, TIFFTAG_IMAGELENGTH, &h);
        TIFFGetField(tif, TIFFTAG_SAMPLESPERPIXEL, &spp);
        TIFFGetField(tif, TIFFTAG_BITSPERSAMPLE, &bps);
        TIFFGetField(tif, TIFFTAG_SAMPLEFORMAT, &fmt);

        if (w > 0 && h > 0 && w <= 10000 && h <= 10000) {
            tmsize_t scanline_size = TIFFScanlineSize(tif);
            if (scanline_size > 0 && scanline_size <= (tmsize_t)(w * spp * (bps / 8) + 16)) {
                uint8_t *buf = (uint8_t *)malloc((size_t)scanline_size);
                if (buf) {
                    for (uint32_t row = 0; row < h; row++) {
                        if (TIFFReadScanline(tif, buf, row, 0) < 0) {
                            break;
                        }
                    }
                    free(buf);
                }
            }
        }
        TIFFClose(tif);
    }

    unlink(filename);
    return 0;
}