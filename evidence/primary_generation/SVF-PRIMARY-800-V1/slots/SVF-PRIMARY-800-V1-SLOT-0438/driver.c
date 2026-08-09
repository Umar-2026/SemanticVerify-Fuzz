#include <tiffio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 10) return 0;

    TIFFSetErrorHandler(NULL);
    TIFFSetWarningHandler(NULL);

    TIFF *tif = TIFFStreamOpen("fuzz.tiff", data, size);
    if (!tif) return 0;

    uint32_t width, height;
    if (TIFFGetField(tif, TIFFTAG_IMAGEWIDTH, &width) &&
        TIFFGetField(tif, TIFFTAG_IMAGELENGTH, &height)) {
        
        tsize_t scanline_size = TIFFScanlineSize(tif);
        if (scanline_size > 0) {
            void *buf = malloc(scanline_size);
            if (buf) {
                for (uint32_t row = 0; row < height && row < 16; row++) {
                    TIFFReadScanline(tif, buf, row, 0);
                }
                free(buf);
            }
        }

        tstrip_t nstrips = TIFFNumberOfStrips(tif);
        tsize_t strip_size = TIFFStripSize(tif);
        if (nstrips > 0 && strip_size > 0) {
            void *strip_buf = malloc(strip_size);
            if (strip_buf) {
                for (tstrip_t s = 0; s < nstrips && s < 4; s++) {
                    TIFFReadEncodedStrip(tif, s, strip_buf, strip_size);
                }
                free(strip_buf);
            }
        }
    }

    TIFFClose(tif);
    return 0;
}