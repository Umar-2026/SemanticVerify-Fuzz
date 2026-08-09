#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <tiffio.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 8) {
        return 0;
    }

    // Create a temporary file to hold the fuzz data
    char filename[] = "/tmp/libtiff_fuzz_XXXXXX";
    int fd = mkstemp(filename);
    if (fd < 0) {
        return 0;
    }
    ssize_t written = write(fd, data, size);
    if (written != (ssize_t)size) {
        close(fd);
        unlink(filename);
        return 0;
    }
    close(fd);

    TIFF *tif = TIFFOpen(filename, "r");
    if (tif == NULL) {
        unlink(filename);
        return 0;
    }

    // Inspect basic image information
    uint32_t width = 0, height = 0;
    uint16_t bits_per_sample = 0, samples_per_pixel = 0;
    uint16_t compression = 0, photometric = 0;
    uint16_t orientation = 0;
    uint32_t rows_per_strip = 0;

    TIFFGetField(tif, TIFFTAG_IMAGEWIDTH, &width);
    TIFFGetField(tif, TIFFTAG_IMAGELENGTH, &height);
    TIFFGetField(tif, TIFFTAG_BITSPERSAMPLE, &bits_per_sample);
    TIFFGetField(tif, TIFFTAG_SAMPLESPERPIXEL, &samples_per_pixel);
    TIFFGetField(tif, TIFFTAG_COMPRESSION, &compression);
    TIFFGetField(tif, TIFFTAG_PHOTOMETRIC, &photometric);
    TIFFGetField(tif, TIFFTAG_ORIENTATION, &orientation);
    TIFFGetField(tif, TIFFTAG_ROWSPERSTRIP, &rows_per_strip);

    // Use the values to prevent optimization
    volatile uint32_t sum = width + height + rows_per_strip;
    volatile uint16_t sum16 = bits_per_sample + samples_per_pixel + compression + photometric + orientation;
    (void)sum;
    (void)sum16;

    TIFFClose(tif);
    unlink(filename);
    return 0;
}