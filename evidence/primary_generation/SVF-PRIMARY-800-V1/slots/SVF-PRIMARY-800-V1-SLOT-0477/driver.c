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
    uint16_t compression, predictor;

    TIFFGetField(in, TIFFTAG_IMAGEWIDTH, &width);
    TIFFGetField(in, TIFFTAG_IMAGELENGTH, &height);
    TIFFGetField(in, TIFFTAG_BITSPERSAMPLE, &bits_per_sample);
    TIFFGetField(in, TIFFTAG_SAMPLESPERPIXEL, &samples_per_pixel);
    TIFFGetField(in, TIFFTAG_PHOTOMETRIC, &photometric);
    TIFFGetField(in, TIFFTAG_PLANARCONFIG, &planar_config);
    TIFFGetField(in, TIFFTAG_COMPRESSION, &compression);
    TIFFGetField(in, TIFFTAG_PREDICTOR, &predictor);

    // Limit dimensions to avoid excessive memory usage
    if (width == 0 || height == 0 || width > 4096 || height > 4096) {
        TIFFClose(in);
        unlink(input_path);
        unlink(output_path);
        return 0;
    }

    tmsize_t scanline_size = TIFFScanlineSize(in);
    if (scanline_size <= 0 || scanline_size > 1024 * 1024) {
        TIFFClose(in);
        unlink(input_path);
        unlink(output_path);
        return 0;
    }

    uint8_t *buffer = (uint8_t *)malloc(scanline_size);
    if (!buffer) {
        TIFFClose(in);
        unlink(input_path);
        unlink(output_path);
        return 0;
    }

    TIFF *out = TIFFOpen(output_path, "w");
    if (!out) {
        free(buffer);
        TIFFClose(in);
        unlink(input_path);
        unlink(output_path);
        return 0;
    }

    TIFFSetField(out, TIFFTAG_IMAGEWIDTH, width);
    TIFFSetField(out, TIFFTAG_IMAGELENGTH, height);
    TIFFSetField(out, TIFFTAG_BITSPERSAMPLE, bits_per_sample);
    TIFFSetField(out, TIFFTAG_SAMPLESPERPIXEL, samples_per_pixel);
    TIFFSetField(out, TIFFTAG_PHOTOMETRIC, photometric);
    TIFFSetField(out, TIFFTAG_PLANARCONFIG, planar_config);
    TIFFSetField(out, TIFFTAG_COMPRESSION, compression);
    TIFFSetField(out, TIFFTAG_PREDICTOR, predictor);
    TIFFSetField(out, TIFFTAG_ROWSPERSTRIP, TIFFDefaultStripSize(out, 0));

    for (uint32_t row = 0; row < height; row++) {
        if (TIFFReadScanline(in, buffer, row, 0) < 0) {
            break;
        }
        if (TIFFWriteScanline(out, buffer, row, 0) < 0) {
            break;
        }
    }

    TIFFClose(out);
    TIFFClose(in);
    free(buffer);
    unlink(input_path);
    unlink(output_path);
    return 0;
}