#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <stdlib.h>
#include "tiffio.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 16) return 0;

    // Use first 4 bytes for width, next 4 for height, next 4 for bits per sample, next 4 for samples per pixel
    uint32_t width = 0, height = 0;
    uint16_t bits_per_sample = 0, samples_per_pixel = 0;
    memcpy(&width, data, 4);
    memcpy(&height, data + 4, 4);
    memcpy(&bits_per_sample, data + 8, 2);
    memcpy(&samples_per_pixel, data + 12, 2);

    // Clamp values to reasonable ranges to avoid excessive memory usage
    if (width > 1024) width = 1024;
    if (height > 1024) height = 1024;
    if (bits_per_sample == 0 || bits_per_sample > 32) bits_per_sample = 8;
    if (samples_per_pixel == 0 || samples_per_pixel > 4) samples_per_pixel = 1;

    // Use remaining data as fuzz-derived field values
    size_t offset = 16;
    uint32_t compression = 1; // default no compression
    uint16_t photometric = 1; // min-is-black
    uint32_t rows_per_strip = 1;
    uint16_t planar_config = 1; // contig
    uint16_t sample_format = 1; // unsigned int

    if (offset + 2 <= size) {
        memcpy(&compression, data + offset, 2);
        offset += 2;
    }
    if (offset + 2 <= size) {
        memcpy(&photometric, data + offset, 2);
        offset += 2;
    }
    if (offset + 4 <= size) {
        memcpy(&rows_per_strip, data + offset, 4);
        offset += 4;
    }
    if (offset + 2 <= size) {
        memcpy(&planar_config, data + offset, 2);
        offset += 2;
    }
    if (offset + 2 <= size) {
        memcpy(&sample_format, data + offset, 2);
        offset += 2;
    }

    // Clamp field values to valid ranges
    if (compression > 5) compression = 1;
    if (photometric > 3) photometric = 1;
    if (rows_per_strip == 0 || rows_per_strip > height) rows_per_strip = height;
    if (planar_config != 1 && planar_config != 2) planar_config = 1;
    if (sample_format != 1 && sample_format != 2 && sample_format != 3) sample_format = 1;

    // Create a temporary file name
    char filename[] = "/tmp/libtiff_fuzz_XXXXXX";
    int fd = mkstemp(filename);
    if (fd < 0) return 0;
    close(fd);

    TIFF *tif = TIFFOpen(filename, "w");
    if (!tif) {
        unlink(filename);
        return 0;
    }

    TIFFSetField(tif, TIFFTAG_IMAGEWIDTH, width);
    TIFFSetField(tif, TIFFTAG_IMAGELENGTH, height);
    TIFFSetField(tif, TIFFTAG_BITSPERSAMPLE, bits_per_sample);
    TIFFSetField(tif, TIFFTAG_SAMPLESPERPIXEL, samples_per_pixel);
    TIFFSetField(tif, TIFFTAG_COMPRESSION, compression);
    TIFFSetField(tif, TIFFTAG_PHOTOMETRIC, photometric);
    TIFFSetField(tif, TIFFTAG_ROWSPERSTRIP, rows_per_strip);
    TIFFSetField(tif, TIFFTAG_PLANARCONFIG, planar_config);
    TIFFSetField(tif, TIFFTAG_SAMPLEFORMAT, sample_format);

    // Compute scanline size in bytes
    tmsize_t scanline_size = TIFFScanlineSize(tif);
    if (scanline_size <= 0) {
        TIFFClose(tif);
        unlink(filename);
        return 0;
    }

    // Allocate buffer for one scanline
    uint8_t *buf = (uint8_t *)malloc(scanline_size);
    if (!buf) {
        TIFFClose(tif);
        unlink(filename);
        return 0;
    }

    // Fill scanline with fuzz data (cycling through input if needed)
    size_t data_index = offset;
    for (tmsize_t i = 0; i < scanline_size; i++) {
        if (data_index >= size) data_index = offset;
        buf[i] = data[data_index++];
    }

    // Write all scanlines
    for (uint32_t row = 0; row < height; row++) {
        if (TIFFWriteScanline(tif, buf, row, 0) < 0) {
            break;
        }
    }

    free(buf);
    TIFFClose(tif);
    unlink(filename);
    return 0;
}