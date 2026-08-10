#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <tiffio.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 8) return 0;

    // Create a temporary input file from fuzz data
    char input_path[] = "/tmp/libtiff_fuzz_input_XXXXXX";
    int input_fd = mkstemp(input_path);
    if (input_fd < 0) return 0;
    write(input_fd, data, size);
    close(input_fd);

    // Create a temporary output file
    char output_path[] = "/tmp/libtiff_fuzz_output_XXXXXX";
    int output_fd = mkstemp(output_path);
    if (output_fd < 0) {
        unlink(input_path);
        return 0;
    }
    close(output_fd);

    TIFF *in = TIFFOpen(input_path, "r");
    if (!in) {
        unlink(input_path);
        unlink(output_path);
        return 0;
    }

    uint32_t width, height;
    uint16_t bits_per_sample, samples_per_pixel;
    uint16_t photometric, planar_config;
    TIFFGetField(in, TIFFTAG_IMAGEWIDTH, &width);
    TIFFGetField(in, TIFFTAG_IMAGELENGTH, &height);
    TIFFGetField(in, TIFFTAG_BITSPERSAMPLE, &bits_per_sample);
    TIFFGetField(in, TIFFTAG_SAMPLESPERPIXEL, &samples_per_pixel);
    TIFFGetField(in, TIFFTAG_PHOTOMETRIC, &photometric);
    TIFFGetField(in, TIFFTAG_PLANARCONFIG, &planar_config);

    // Validate dimensions to avoid excessive memory usage
    if (width == 0 || height == 0 || width > 4096 || height > 4096) {
        TIFFClose(in);
        unlink(input_path);
        unlink(output_path);
        return 0;
    }

    // Compute scanline size in bytes
    tmsize_t scanline_size = TIFFScanlineSize(in);
    if (scanline_size <= 0) {
        TIFFClose(in);
        unlink(input_path);
        unlink(output_path);
        return 0;
    }

    // Allocate buffer for one scanline
    uint8_t *buf = (uint8_t *)malloc(scanline_size);
    if (!buf) {
        TIFFClose(in);
        unlink(input_path);
        unlink(output_path);
        return 0;
    }

    // Open output TIFF
    TIFF *out = TIFFOpen(output_path, "w");
    if (!out) {
        free(buf);
        TIFFClose(in);
        unlink(input_path);
        unlink(output_path);
        return 0;
    }

    // Copy essential tags
    TIFFSetField(out, TIFFTAG_IMAGEWIDTH, width);
    TIFFSetField(out, TIFFTAG_IMAGELENGTH, height);
    TIFFSetField(out, TIFFTAG_BITSPERSAMPLE, bits_per_sample);
    TIFFSetField(out, TIFFTAG_SAMPLESPERPIXEL, samples_per_pixel);
    TIFFSetField(out, TIFFTAG_PHOTOMETRIC, photometric);
    TIFFSetField(out, TIFFTAG_PLANARCONFIG, planar_config);
    TIFFSetField(out, TIFFTAG_ROWSPERSTRIP, height); // single strip for simplicity

    // Read and write scanlines
    for (uint32_t row = 0; row < height; row++) {
        if (TIFFReadScanline(in, buf, row, 0) < 0) {
            break;
        }
        if (TIFFWriteScanline(out, buf, row, 0) < 0) {
            break;
        }
    }

    TIFFClose(out);
    TIFFClose(in);
    free(buf);
    unlink(input_path);
    unlink(output_path);
    return 0;
}