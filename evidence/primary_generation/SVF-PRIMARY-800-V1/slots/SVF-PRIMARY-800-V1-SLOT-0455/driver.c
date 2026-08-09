#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <tiffio.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

    // Create a temporary file to hold the input data
    char filename[] = "/tmp/libtiff_fuzz_XXXXXX";
    int fd = mkstemp(filename);
    if (fd < 0) return 0;
    size_t written = 0;
    while (written < size) {
        ssize_t n = write(fd, data + written, size - written);
        if (n <= 0) break;
        written += (size_t)n;
    }
    close(fd);

    TIFF *tif = TIFFOpen(filename, "r");
    unlink(filename);
    if (!tif) return 0;

    uint32_t width, height;
    uint16_t bits_per_sample, samples_per_pixel;
    TIFFGetField(tif, TIFFTAG_IMAGEWIDTH, &width);
    TIFFGetField(tif, TIFFTAG_IMAGELENGTH, &height);
    TIFFGetField(tif, TIFFTAG_BITSPERSAMPLE, &bits_per_sample);
    TIFFGetField(tif, TIFFTAG_SAMPLESPERPIXEL, &samples_per_pixel);

    // Compute scanline size dynamically
    tmsize_t scanline_size = TIFFScanlineSize(tif);
    if (scanline_size <= 0) {
        TIFFClose(tif);
        return 0;
    }

    // Allocate buffer for one scanline
    uint8_t *buf = (uint8_t *)malloc((size_t)scanline_size);
    if (!buf) {
        TIFFClose(tif);
        return 0;
    }

    // Read all scanlines
    for (uint32_t row = 0; row < height; row++) {
        if (TIFFReadScanline(tif, buf, row, 0) < 0) {
            break;
        }
        // Inspect the data: compute a simple checksum to force reading
        volatile uint32_t sum = 0;
        for (tmsize_t i = 0; i < scanline_size; i++) {
            sum += buf[i];
        }
        (void)sum;
    }

    free(buf);
    TIFFClose(tif);
    return 0;
}