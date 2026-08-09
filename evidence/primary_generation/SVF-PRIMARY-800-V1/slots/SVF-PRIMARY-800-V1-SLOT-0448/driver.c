#include <tiffio.h>
#include <stdint.h>
#include <stdlib.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 10) {
        return 0;
    }

    TIFF *tif = TIFFStreamOpen("fuzz", data, size);
    if (!tif) {
        return 0;
    }

    uint32_t width, height;
    int dir_count = 0;

    do {
        if (TIFFGetField(tif, TIFFTAG_IMAGEWIDTH, &width) &&
            TIFFGetField(tif, TIFFTAG_IMAGELENGTH, &height)) {
            
            if (width > 0 && height > 0) {
                uint32_t *raster = (uint32_t *)_TIFFmalloc(width * height * sizeof(uint32_t));
                if (raster) {
                    TIFFReadRGBAImage(tif, width, height, raster, 0);
                    _TIFFfree(raster);
                }
            }
        }
        dir_count++;
    } while (TIFFReadDirectory(tif) && dir_count < 10);

    TIFFClose(tif);
    return 0;
}