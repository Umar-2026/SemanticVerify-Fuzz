#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
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
    uint16_t photometric = 0;
    uint32_t rows_per_strip = 0;
    uint32_t strips_per_image = 0;

    TIFFGetField(tif, TIFFTAG_IMAGEWIDTH, &width);
    TIFFGetField(tif, TIFFTAG_IMAGELENGTH, &height);
    TIFFGetField(tif, TIFFTAG_BITSPERSAMPLE, &bits_per_sample);
    TIFFGetField(tif, TIFFTAG_SAMPLESPERPIXEL, &samples_per_pixel);
    TIFFGetField(tif, TIFFTAG_PHOTOMETRIC, &photometric);
    TIFFGetField(tif, TIFFTAG_ROWSPERSTRIP, &rows_per_strip);

    if (width == 0 || height == 0 || rows_per_strip == 0) {
        TIFFClose(tif);
        unlink(filename);
        return 0;
    }

    // Compute number of strips
    strips_per_image = (height + rows_per_strip - 1) / rows_per_strip;

    // Attempt to read representative image data: read a few strips from the middle
    // Limit to at most 4 strips to keep the fuzzer bounded
    uint32_t start_strip = strips_per_image / 2;
    uint32_t num_strips = strips_per_image - start_strip;
    if (num_strips > 4) num_strips = 4;

    // Allocate a buffer for one strip
    tmsize_t strip_size = TIFFStripSize(tif);
    if (strip_size <= 0) {
        TIFFClose(tif);
        unlink(filename);
        return 0;
    }

    unsigned char *buf = (unsigned char *)malloc(strip_size);
    if (!buf) {
        TIFFClose(tif);
        unlink(filename);
        return 0;
    }

    for (uint32_t i = 0; i < num_strips; i++) {
        uint32_t strip = start_strip + i;
        if (strip >= strips_per_image) break;
        TIFFReadEncodedStrip(tif, strip, buf, strip_size);
    }

    free(buf);
    TIFFClose(tif);
    unlink(filename);
    return 0;
}