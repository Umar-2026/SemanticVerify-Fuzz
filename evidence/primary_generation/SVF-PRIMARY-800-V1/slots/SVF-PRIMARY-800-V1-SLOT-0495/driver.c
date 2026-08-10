#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <tiffio.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 8) return 0;

    // Create a temporary file to hold the input data
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
    if (!tif) {
        unlink(filename);
        return 0;
    }

    // Inspect image metadata
    uint32_t width = 0, height = 0;
    uint16_t bits_per_sample = 0, samples_per_pixel = 0;
    uint16_t planar_config = 0;
    uint32_t rows_per_strip = 0;
    uint32_t strips_per_image = 0;

    TIFFGetField(tif, TIFFTAG_IMAGEWIDTH, &width);
    TIFFGetField(tif, TIFFTAG_IMAGELENGTH, &height);
    TIFFGetField(tif, TIFFTAG_BITSPERSAMPLE, &bits_per_sample);
    TIFFGetField(tif, TIFFTAG_SAMPLESPERPIXEL, &samples_per_pixel);
    TIFFGetField(tif, TIFFTAG_PLANARCONFIG, &planar_config);
    TIFFGetField(tif, TIFFTAG_ROWSPERSTRIP, &rows_per_strip);

    if (width == 0 || height == 0 || rows_per_strip == 0) {
        TIFFClose(tif);
        unlink(filename);
        return 0;
    }

    strips_per_image = (height + rows_per_strip - 1) / rows_per_strip;

    // Attempt to read representative image data from a few strips
    // Limit the number of strips read to avoid excessive work
    uint32_t max_strips = strips_per_image < 4 ? strips_per_image : 4;
    for (uint32_t s = 0; s < max_strips; s++) {
        tmsize_t strip_size = TIFFStripSize(tif);
        if (strip_size <= 0) break;
        // Allocate a buffer for the strip data
        unsigned char *buf = (unsigned char *)malloc(strip_size);
        if (!buf) break;
        if (TIFFReadEncodedStrip(tif, s, buf, strip_size) < 0) {
            free(buf);
            break;
        }
        free(buf);
    }

    TIFFClose(tif);
    unlink(filename);
    return 0;
}