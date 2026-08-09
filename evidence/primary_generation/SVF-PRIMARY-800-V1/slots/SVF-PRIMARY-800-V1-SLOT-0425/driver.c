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
        uint32_t width = 0, height = 0;
        uint16_t bits_per_sample = 0, samples_per_pixel = 0;
        uint16_t photometric = 0;
        uint32_t *raster = NULL;

        TIFFGetField(tif, TIFFTAG_IMAGEWIDTH, &width);
        TIFFGetField(tif, TIFFTAG_IMAGELENGTH, &height);
        TIFFGetField(tif, TIFFTAG_BITSPERSAMPLE, &bits_per_sample);
        TIFFGetField(tif, TIFFTAG_SAMPLESPERPIXEL, &samples_per_pixel);
        TIFFGetField(tif, TIFFTAG_PHOTOMETRIC, &photometric);

        // Basic sanity checks to avoid huge allocations
        if (width > 0 && height > 0 && width <= 10000 && height <= 10000 &&
            bits_per_sample > 0 && bits_per_sample <= 64 &&
            samples_per_pixel > 0 && samples_per_pixel <= 4) {
            size_t raster_size = (size_t)width * height * sizeof(uint32_t);
            if (raster_size / sizeof(uint32_t) == (size_t)width * height) {
                raster = (uint32_t *)_TIFFmalloc(raster_size);
                if (raster) {
                    if (TIFFReadRGBAImage(tif, width, height, raster, 0)) {
                        // Inspect a few pixels to ensure the data is accessible
                        volatile uint32_t sum = 0;
                        for (uint32_t i = 0; i < width && i < 10; i++) {
                            sum += raster[i];
                        }
                        (void)sum;
                    }
                    _TIFFfree(raster);
                }
            }
        }
        TIFFClose(tif);
    }

    unlink(filename);
    return 0;
}