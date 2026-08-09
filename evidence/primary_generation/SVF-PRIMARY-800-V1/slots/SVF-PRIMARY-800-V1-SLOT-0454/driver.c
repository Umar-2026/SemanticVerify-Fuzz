#include <stdint.h>
#include <stdlib.h>
#include <tiffio.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1) return 0;

    TIFF *tif = TIFFFdOpen(0, "fuzz_input", "r");
    if (!tif) return 0;

    uint32_t width, height;
    TIFFGetField(tif, TIFFTAG_IMAGEWIDTH, &width);
    TIFFGetField(tif, TIFFTAG_IMAGELENGTH, &height);

    tsize_t scanline_size = TIFFScanlineSize(tif);
    if (scanline_size <= 0) {
        TIFFClose(tif);
        return 0;
    }

    void *buf = malloc(scanline_size);
    if (!buf) {
        TIFFClose(tif);
        return 0;
    }

    for (uint32_t row = 0; row < height; row++) {
        if (TIFFReadScanline(tif, buf, row, 0) < 0) {
            break;
        }
    }

    free(buf);
    TIFFClose(tif);
    return 0;
}