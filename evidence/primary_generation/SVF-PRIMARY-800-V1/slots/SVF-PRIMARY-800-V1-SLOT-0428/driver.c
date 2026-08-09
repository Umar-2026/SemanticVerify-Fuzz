#include <tiffio.h>
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1) {
        return 0;
    }

    char filename[] = "/tmp/fuzz.tiff";
    FILE *fp = fopen(filename, "wb");
    if (!fp) {
        return 0;
    }
    fwrite(data, 1, size, fp);
    fclose(fp);

    TIFFSetErrorHandler(NULL);
    TIFFSetWarningHandler(NULL);

    TIFF *tif = TIFFOpen(filename, "r");
    if (tif) {
        uint32_t width, height;
        if (TIFFGetField(tif, TIFFTAG_IMAGEWIDTH, &width) &&
            TIFFGetField(tif, TIFFTAG_IMAGELENGTH, &height)) {
            
            if (width > 0 && height > 0 && width < 10000 && height < 10000) {
                size_t npixels = (size_t)width * height;
                uint32_t *raster = (uint32_t *)_TIFFmalloc(npixels * sizeof(uint32_t));
                if (raster != NULL) {
                    if (TIFFReadRGBAImage(tif, width, height, raster, 0)) {
                        // Accessing content to trigger potential memory issues
                        volatile uint32_t pixel = raster[0];
                        (void)pixel;
                    }
                    _TIFFfree(raster);
                }
            }
        }
        TIFFClose(tif);
    }

    remove(filename);
    return 0;
}