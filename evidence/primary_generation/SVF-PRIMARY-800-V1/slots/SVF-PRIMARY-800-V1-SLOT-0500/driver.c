#include <tiffio.h>
#include <stdint.h>
#include <stdlib.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 10) {
        return 0;
    }

    char filename[] = "/tmp/fuzz.tiff";
    FILE *fp = fopen(filename, "wb");
    if (!fp) return 0;
    fwrite(data, 1, size, fp);
    fclose(fp);

    TIFFSetErrorHandler(NULL);
    TIFFSetWarningHandler(NULL);

    TIFF *tif = TIFFOpen(filename, "r");
    if (tif) {
        uint32_t width = 0, height = 0;
        uint16_t samplesperpixel = 0;

        TIFFGetField(tif, TIFFTAG_IMAGEWIDTH, &width);
        TIFFGetField(tif, TIFFTAG_IMAGELENGTH, &height);
        TIFFGetField(tif, TIFFTAG_SAMPLESPERPIXEL, &samplesperpixel);

        if (width > 0 && height > 0) {
            tsize_t stripSize = TIFFStripSize(tif);
            void *buf = _TIFFmalloc(stripSize);
            if (buf) {
                uint32_t nStrips = TIFFNumberOfStrips(tif);
                for (uint32_t i = 0; i < nStrips && i < 10; i++) {
                    TIFFReadEncodedStrip(tif, i, buf, stripSize);
                }
                _TIFFfree(buf);
            }
        }
        TIFFClose(tif);
    }

    remove(filename);
    return 0;
}