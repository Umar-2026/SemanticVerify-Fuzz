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

    // Write first half to a temp file
    char path1[] = "/tmp/fuzz_tiff_XXXXXX";
    int fd1 = mkstemp(path1);
    if (fd1 < 0) return 0;
    FILE *f1 = fdopen(fd1, "wb");
    if (!f1) { close(fd1); unlink(path1); return 0; }
    fwrite(data1, 1, size1, f1);
    fclose(f1);

    // Write second half to a temp file
    char path2[] = "/tmp/fuzz_tiff_XXXXXX";
    int fd2 = mkstemp(path2);
    if (fd2 < 0) { unlink(path1); return 0; }
    FILE *f2 = fdopen(fd2, "wb");
    if (!f2) { close(fd2); unlink(path1); unlink(path2); return 0; }
    fwrite(data2, 1, size2, f2);
    fclose(f2);

    // Open both TIFF files
    TIFF *tif1 = TIFFOpen(path1, "r");
    TIFF *tif2 = TIFFOpen(path2, "r");

    if (tif1) {
        uint32_t w = 0, h = 0;
        uint16_t bps = 0, spp = 0, comp = 0, photometric = 0;
        TIFFGetField(tif1, TIFFTAG_IMAGEWIDTH, &w);
        TIFFGetField(tif1, TIFFTAG_IMAGELENGTH, &h);
        TIFFGetField(tif1, TIFFTAG_BITSPERSAMPLE, &bps);
        TIFFGetField(tif1, TIFFTAG_SAMPLESPERPIXEL, &spp);
        TIFFGetField(tif1, TIFFTAG_COMPRESSION, &comp);
        TIFFGetField(tif1, TIFFTAG_PHOTOMETRIC, &photometric);
        // Use the values to prevent optimization
        volatile uint32_t sum = w + h + bps + spp + comp + photometric;
        (void)sum;
        TIFFClose(tif1);
    }

    if (tif2) {
        uint32_t w = 0, h = 0;
        uint16_t bps = 0, spp = 0, comp = 0, photometric = 0;
        TIFFGetField(tif2, TIFFTAG_IMAGEWIDTH, &w);
        TIFFGetField(tif2, TIFFTAG_IMAGELENGTH, &h);
        TIFFGetField(tif2, TIFFTAG_BITSPERSAMPLE, &bps);
        TIFFGetField(tif2, TIFFTAG_SAMPLESPERPIXEL, &spp);
        TIFFGetField(tif2, TIFFTAG_COMPRESSION, &comp);
        TIFFGetField(tif2, TIFFTAG_PHOTOMETRIC, &photometric);
        volatile uint32_t sum = w + h + bps + spp + comp + photometric;
        (void)sum;
        TIFFClose(tif2);
    }

    // Clean up temp files
    unlink(path1);
    unlink(path2);

    return 0;
}