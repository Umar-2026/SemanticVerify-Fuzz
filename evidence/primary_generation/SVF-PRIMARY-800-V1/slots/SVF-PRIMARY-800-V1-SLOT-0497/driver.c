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

    TIFFGetField(tif, TIFFTAG_IMAGEWIDTH, &width);
    TIFFGetField(tif, TIFFTAG_IMAGELENGTH, &height);
    TIFFGetField(tif, TIFFTAG_BITSPERSAMPLE, &bits_per_sample);
    TIFFGetField(tif, TIFFTAG_SAMPLESPERPIXEL, &samples_per_pixel);
    TIFFGetField(tif, TIFFTAG_PHOTOMETRIC, &photometric);
    TIFFGetField(tif, TIFFTAG_ROWSPERSTRIP, &rows_per_strip);

    // If no rows per strip, use default (assume whole image)
    if (rows_per_strip == 0) {
        rows_per_strip = height > 0 ? height : 1;
    }

    // Compute strip size safely
    uint64_t strip_size = 0;
    if (width > 0 && height > 0 && bits_per_sample > 0 && samples_per_pixel > 0) {
        uint64_t row_bytes = ((uint64_t)width * bits_per_sample * samples_per_pixel + 7) / 8;
        strip_size = row_bytes * rows_per_strip;
    }

    // Limit allocation to avoid excessive memory usage
    if (strip_size > 1024 * 1024 * 16) {
        strip_size = 1024 * 1024 * 16;
    }

    if (strip_size > 0) {
        uint8_t *buf = (uint8_t *)malloc(strip_size);
        if (buf) {
            // Read a few strips (up to 4) to exercise the decoder
            tstrip_t num_strips = TIFFNumberOfStrips(tif);
            for (tstrip_t s = 0; s < num_strips && s < 4; s++) {
                tmsize_t read_size = TIFFReadEncodedStrip(tif, s, buf, (tmsize_t)strip_size);
                (void)read_size;
            }
            free(buf);
        }
    }

    TIFFClose(tif);
    unlink(filename);
    return 0;
}