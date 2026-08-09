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

    // Create temporary files for the two TIFF sources
    char path1[] = "/tmp/libtiff_fuzz_s07_1_XXXXXX";
    char path2[] = "/tmp/libtiff_fuzz_s07_2_XXXXXX";
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

    if (tif1 && tif2) {
        // Inspect basic information from each
        uint32_t w1 = 0, h1 = 0, w2 = 0, h2 = 0;
        uint16_t bps1 = 0, spp1 = 0, bps2 = 0, spp2 = 0;
        uint16_t comp1 = 0, comp2 = 0;
        uint16_t photometric1 = 0, photometric2 = 0;

        TIFFGetField(tif1, TIFFTAG_IMAGEWIDTH, &w1);
        TIFFGetField(tif1, TIFFTAG_IMAGELENGTH, &h1);
        TIFFGetField(tif1, TIFFTAG_BITSPERSAMPLE, &bps1);
        TIFFGetField(tif1, TIFFTAG_SAMPLESPERPIXEL, &spp1);
        TIFFGetField(tif1, TIFFTAG_COMPRESSION, &comp1);
        TIFFGetField(tif1, TIFFTAG_PHOTOMETRIC, &photometric1);

        TIFFGetField(tif2, TIFFTAG_IMAGEWIDTH, &w2);
        TIFFGetField(tif2, TIFFTAG_IMAGELENGTH, &h2);
        TIFFGetField(tif2, TIFFTAG_BITSPERSAMPLE, &bps2);
        TIFFGetField(tif2, TIFFTAG_SAMPLESPERPIXEL, &spp2);
        TIFFGetField(tif2, TIFFTAG_COMPRESSION, &comp2);
        TIFFGetField(tif2, TIFFTAG_PHOTOMETRIC, &photometric2);

        // Use the values to force some computation (avoid optimization)
        volatile uint32_t sum = w1 + h1 + w2 + h2;
        sum += bps1 + spp1 + comp1 + photometric1;
        sum += bps2 + spp2 + comp2 + photometric2;
        (void)sum;
    }

    // Clean up
    if (tif1) TIFFClose(tif1);
    if (tif2) TIFFClose(tif2);
    unlink(path1);
    unlink(path2);

    return 0;
}