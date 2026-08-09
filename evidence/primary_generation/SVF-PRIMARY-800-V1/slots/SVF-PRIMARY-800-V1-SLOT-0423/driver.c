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
        uint16_t samples_per_pixel = 0, bits_per_sample = 0;
        uint16_t planar_config = 0;
        uint32_t *raster = NULL;

        TIFFGetField(tif, TIFFTAG_IMAGEWIDTH, &width);
        TIFFGetField(tif, TIFFTAG_IMAGELENGTH, &height);
        TIFFGetField(tif, TIFFTAG_SAMPLESPERPIXEL, &samples_per_pixel);
        TIFFGetField(tif, TIFFTAG_BITSPERSAMPLE, &bits_per_sample);
        TIFFGetField(tif, TIFFTAG_PLANARCONFIG, &planar_config);

        // Basic sanity checks to avoid excessive allocation
        if (width > 0 && height > 0 && width <= 10000 && height <= 10000 &&
            samples_per_pixel > 0 && samples_per_pixel <= 4 &&
            bits_per_sample == 8 && planar_config == PLANARCONFIG_CONTIG) {
            size_t npixels = (size_t)width * height;
            raster = (uint32_t *)malloc(npixels * sizeof(uint32_t));
            if (raster) {
                if (TIFFReadRGBAImage(tif, width, height, raster, 0)) {
                    // Inspect a few pixels to ensure the data is accessible
                    volatile uint32_t sum = 0;
                    for (size_t i = 0; i < npixels && i < 1024; i++) {
                        sum += raster[i];
                    }
                    (void)sum;
                }
                free(raster);
            }
        }

        TIFFClose(tif);
    }

    unlink(filename);
    return 0;
}