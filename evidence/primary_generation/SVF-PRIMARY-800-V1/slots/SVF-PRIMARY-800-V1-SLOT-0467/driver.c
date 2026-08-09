#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <tiffio.h>

static void write_tiff_data(const uint8_t *data, size_t size, const char *path) {
    FILE *f = fopen(path, "wb");
    if (!f) return;
    fwrite(data, 1, size, f);
    fclose(f);
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

    // Split input into two halves
    size_t half = size / 2;
    const uint8_t *data1 = data;
    size_t size1 = half;
    const uint8_t *data2 = data + half;
    size_t size2 = size - half;

    // Write to temporary files
    const char *path1 = "/tmp/fuzz_tiff_1.tif";
    const char *path2 = "/tmp/fuzz_tiff_2.tif";
    write_tiff_data(data1, size1, path1);
    write_tiff_data(data2, size2, path2);

    // Open both TIFF files
    TIFF *tif1 = TIFFOpen(path1, "r");
    TIFF *tif2 = TIFFOpen(path2, "r");

    if (tif1 && tif2) {
        uint32_t w1 = 0, h1 = 0, w2 = 0, h2 = 0;
        uint16_t bps1 = 0, spp1 = 0, bps2 = 0, spp2 = 0;

        TIFFGetField(tif1, TIFFTAG_IMAGEWIDTH, &w1);
        TIFFGetField(tif1, TIFFTAG_IMAGELENGTH, &h1);
        TIFFGetField(tif1, TIFFTAG_BITSPERSAMPLE, &bps1);
        TIFFGetField(tif1, TIFFTAG_SAMPLESPERPIXEL, &spp1);

        TIFFGetField(tif2, TIFFTAG_IMAGEWIDTH, &w2);
        TIFFGetField(tif2, TIFFTAG_IMAGELENGTH, &h2);
        TIFFGetField(tif2, TIFFTAG_BITSPERSAMPLE, &bps2);
        TIFFGetField(tif2, TIFFTAG_SAMPLESPERPIXEL, &spp2);

        // Compare dimensions and samples
        if (w1 == w2 && h1 == h2 && bps1 == bps2 && spp1 == spp2) {
            // Read a scanline from each and compare
            tmsize_t scanline_size1 = TIFFScanlineSize(tif1);
            tmsize_t scanline_size2 = TIFFScanlineSize(tif2);
            if (scanline_size1 > 0 && scanline_size2 > 0 && scanline_size1 == scanline_size2) {
                uint8_t *buf1 = (uint8_t *)malloc(scanline_size1);
                uint8_t *buf2 = (uint8_t *)malloc(scanline_size2);
                if (buf1 && buf2) {
                    for (uint32_t row = 0; row < h1 && row < h2; row++) {
                        if (TIFFReadScanline(tif1, buf1, row, 0) < 0) break;
                        if (TIFFReadScanline(tif2, buf2, row, 0) < 0) break;
                        if (memcmp(buf1, buf2, scanline_size1) != 0) {
                            break;
                        }
                    }
                }
                free(buf1);
                free(buf2);
            }
        }
    }

    if (tif1) TIFFClose(tif1);
    if (tif2) TIFFClose(tif2);

    // Clean up temporary files
    remove(path1);
    remove(path2);

    return 0;
}