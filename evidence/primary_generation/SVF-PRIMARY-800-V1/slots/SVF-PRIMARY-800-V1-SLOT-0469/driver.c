#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <tiffio.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

    // Split input into two halves for two independent TIFF files
    size_t half = size / 2;
    const uint8_t *data1 = data;
    size_t size1 = half;
    const uint8_t *data2 = data + half;
    size_t size2 = size - half;

    // Create temporary files for each half
    char path1[] = "/tmp/libtiff_fuzz_XXXXXX";
    char path2[] = "/tmp/libtiff_fuzz_XXXXXX";
    int fd1 = mkstemp(path1);
    int fd2 = mkstemp(path2);
    if (fd1 < 0 || fd2 < 0) {
        if (fd1 >= 0) close(fd1);
        if (fd2 >= 0) close(fd2);
        return 0;
    }

    // Write data to temp files
    ssize_t written1 = write(fd1, data1, size1);
    ssize_t written2 = write(fd2, data2, size2);
    close(fd1);
    close(fd2);
    if (written1 != (ssize_t)size1 || written2 != (ssize_t)size2) {
        unlink(path1);
        unlink(path2);
        return 0;
    }

    // Open both TIFF files
    TIFF *tif1 = TIFFOpen(path1, "r");
    TIFF *tif2 = TIFFOpen(path2, "r");

    if (tif1) {
        // Inspect basic information from first file
        uint32_t w = 0, h = 0;
        uint16_t bits = 0, samples = 0;
        TIFFGetField(tif1, TIFFTAG_IMAGEWIDTH, &w);
        TIFFGetField(tif1, TIFFTAG_IMAGELENGTH, &h);
        TIFFGetField(tif1, TIFFTAG_BITSPERSAMPLE, &bits);
        TIFFGetField(tif1, TIFFTAG_SAMPLESPERPIXEL, &samples);
        // Consume some data to ensure the fields are used
        if (w > 0 && h > 0 && bits > 0 && samples > 0) {
            // Just a dummy operation to use the values
            volatile uint32_t sum = w + h + bits + samples;
            (void)sum;
        }
        TIFFClose(tif1);
    }

    if (tif2) {
        // Inspect basic information from second file
        uint32_t w = 0, h = 0;
        uint16_t bits = 0, samples = 0;
        TIFFGetField(tif2, TIFFTAG_IMAGEWIDTH, &w);
        TIFFGetField(tif2, TIFFTAG_IMAGELENGTH, &h);
        TIFFGetField(tif2, TIFFTAG_BITSPERSAMPLE, &bits);
        TIFFGetField(tif2, TIFFTAG_SAMPLESPERPIXEL, &samples);
        if (w > 0 && h > 0 && bits > 0 && samples > 0) {
            volatile uint32_t sum = w + h + bits + samples;
            (void)sum;
        }
        TIFFClose(tif2);
    }

    // Cleanup temp files
    unlink(path1);
    unlink(path2);

    return 0;
}