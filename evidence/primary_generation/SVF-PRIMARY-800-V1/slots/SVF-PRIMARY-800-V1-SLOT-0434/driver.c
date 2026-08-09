#include <stdint.h>
#include <stddef.h>
#include <tiffio.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    TIFF *tif = TIFFStreamOpen("fuzz_mem", (void *)data, size);
    if (!tif) {
        return 0;
    }

    uint32_t width, height;
    if (TIFFGetField(tif, TIFFTAG_IMAGEWIDTH, &width) &&
        TIFFGetField(tif, TIFFTAG_IMAGELENGTH, &height)) {
        
        tsize_t scanline_size = TIFFScanlineSize(tif);
        if (scanline_size > 0) {
            void *buf = _TIFFmalloc(scanline_size);
            if (buf) {
                for (uint32_t row = 0; row < height && row < 10; row++) {
                    TIFFReadScanline(tif, buf, row, 0);
                }
                _TIFFfree(buf);
            }
        }

        tstrip_t nstrips = TIFFNumberOfStrips(tif);
        if (nstrips > 0) {
            tsize_t strip_size = TIFFStripSize(tif);
            if (strip_size > 0) {
                void *strip_buf = _TIFFmalloc(strip_size);
                if (strip_buf) {
                    for (tstrip_t s = 0; s < nstrips && s < 5; s++) {
                        TIFFReadEncodedStrip(tif, s, strip_buf, strip_size);
                    }
                    _TIFFfree(strip_buf);
                }
            }
        }
    }

    TIFFClose(tif);
    return 0;
}