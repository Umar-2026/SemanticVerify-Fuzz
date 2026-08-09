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
    unlink(filename);
    if (!tif) return 0;

    uint32_t width, height;
    uint16_t bits_per_sample, samples_per_pixel;
    if (!TIFFGetField(tif, TIFFTAG_IMAGEWIDTH, &width) ||
        !TIFFGetField(tif, TIFFTAG_IMAGELENGTH, &height) ||
        !TIFFGetField(tif, TIFFTAG_BITSPERSAMPLE, &bits_per_sample) ||
        !TIFFGetField(tif, TIFFTAG_SAMPLESPERPIXEL, &samples_per_pixel)) {
        TIFFClose(tif);
        return 0;
    }

    // Guard against excessive allocation
    if (width == 0 || height == 0 || width > 100000 || height > 100000 ||
        bits_per_sample == 0 || samples_per_pixel == 0) {
        TIFFClose(tif);
        return 0;
    }

    tmsize_t scanline_size = TIFFScanlineSize(tif);
    if (scanline_size <= 0) {
        TIFFClose(tif);
        return 0;
    }

    // Allocate a dynamically sized scanline buffer
    uint8_t *buf = (uint8_t *)malloc((size_t)scanline_size);
    if (!buf) {
        TIFFClose(tif);
        return 0;
    }

    // Read each scanline and inspect the data
    for (uint32_t row = 0; row < height; row++) {
        if (TIFFReadScanline(tif, buf, row, 0) < 0) {
            break;
        }
        // Simple inspection: compute a checksum of the scanline data
        volatile uint32_t checksum = 0;
        for (tmsize_t i = 0; i < scanline_size; i++) {
            checksum += buf[i];
        }
        (void)checksum;
    }

    free(buf);
    TIFFClose(tif);
    return 0;
}