#include <tiffio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 10) {
        return 0;
    }

    char filename[] = "/tmp/fuzz.tiff";
    FILE *fp = fopen(filename, "wb");
    if (!fp) {
        return 0;
    }
    fwrite(data, 1, size, fp);
    fclose(fp);

    TIFF *tif = TIFFOpen(filename, "r");
    if (tif) {
        uint32_t width, height;
        TIFFGetField(tif, TIFFTAG_IMAGEWIDTH, &width);
        TIFFGetField(tif, TIFFTAG_IMAGELENGTH, &height);

        if (width > 0 && height > 0) {
            tsize_t scanline_size = TIFFScanlineSize(tif);
            if (scanline_size > 0) {
                void *buf = _TIFFmalloc(scanline_size);
                if (buf) {
                    for (uint32_t row = 0; row < height; row++) {
                        if (TIFFReadScanline(tif, buf, row, 0) < 0) {
                            break;
                        }
                    }
                    _TIFFfree(buf);
                }
            }
        }
        TIFFClose(tif);
    }

    remove(filename);
    return 0;
}