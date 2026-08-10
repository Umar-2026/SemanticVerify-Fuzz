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
    unlink(filename);
    if (!tif) return 0;

    // Read metadata
    uint32_t width = 0, height = 0;
    uint16_t bits_per_sample = 0, samples_per_pixel = 0;
    uint16_t photometric = 0;
    uint32_t rows_per_strip = 0;
    TIFFGetField(tif, TIFFTAG_IMAGEWIDTH, &width);
    TIFFGetField(tif, TIFFTAG_IMAGELENGTH, &height);
    TIFFGetField(tif, TIFFTAG_BITSPERSAMPLE, &bits_per_sample);
    TIFFGetField(tif, TIFFTAG_SAMPLESPERPIXEL, &samples_per_pixel);
    TIFFGetField(tif, TIFFTAG_PHOTOMETRIC, &photometric);
    TIFFGetField(tif, TIFFTAG_ROWSPERSTRIP, &rows_per_strip);

    if (width == 0 || height == 0 || rows_per_strip == 0) {
        TIFFClose(tif);
        return 0;
    }

    // Compute strip size and allocate buffer
    tmsize_t strip_size = TIFFStripSize(tif);
    if (strip_size <= 0) {
        TIFFClose(tif);
        return 0;
    }

    uint8_t *buf = (uint8_t *)malloc(strip_size);
    if (!buf) {
        TIFFClose(tif);
        return 0;
    }

    // Read a representative strip (e.g., the first strip)
    tstrip_t strip_count = TIFFNumberOfStrips(tif);
    if (strip_count > 0) {
        TIFFReadEncodedStrip(tif, 0, buf, strip_size);
    }

    free(buf);
    TIFFClose(tif);
    return 0;
}