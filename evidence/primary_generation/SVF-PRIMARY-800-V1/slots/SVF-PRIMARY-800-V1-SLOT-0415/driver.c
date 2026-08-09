#include <stdint.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <tiffio.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 8) return 0;

    // Use first 4 bytes for width, next 4 for height (small values)
    uint32_t width = data[0] | (data[1] << 8) | (data[2] << 16) | (data[3] << 24);
    uint32_t height = data[4] | (data[5] << 8) | (data[6] << 16) | (data[7] << 24);
    width %= 256;
    height %= 256;
    if (width == 0 || height == 0) return 0;

    // Remaining bytes are used for field values and pixel data
    size_t offset = 8;
    size_t remaining = size - offset;

    // Create a temporary file
    char filename[] = "/tmp/libtiff_fuzz_XXXXXX";
    int fd = mkstemp(filename);
    if (fd < 0) return 0;
    close(fd);

    TIFF *tif = TIFFOpen(filename, "w");
    if (!tif) {
        unlink(filename);
        return 0;
    }

    // Set basic fields
    TIFFSetField(tif, TIFFTAG_IMAGEWIDTH, width);
    TIFFSetField(tif, TIFFTAG_IMAGELENGTH, height);
    TIFFSetField(tif, TIFFTAG_BITSPERSAMPLE, 8);
    TIFFSetField(tif, TIFFTAG_SAMPLESPERPIXEL, 1);
    TIFFSetField(tif, TIFFTAG_ROWSPERSTRIP, height);
    TIFFSetField(tif, TIFFTAG_PLANARCONFIG, PLANARCONFIG_CONTIG);
    TIFFSetField(tif, TIFFTAG_PHOTOMETRIC, PHOTOMETRIC_MINISBLACK);
    TIFFSetField(tif, TIFFTAG_COMPRESSION, COMPRESSION_NONE);
    TIFFSetField(tif, TIFFTAG_ORIENTATION, ORIENTATION_TOPLEFT);

    // Set a few fuzz-derived optional fields if enough data
    if (remaining >= 4) {
        uint16_t compression = data[offset] | (data[offset+1] << 8);
        offset += 2;
        remaining -= 2;
        if (compression == COMPRESSION_NONE || compression == COMPRESSION_LZW ||
            compression == COMPRESSION_DEFLATE || compression == COMPRESSION_PACKBITS) {
            TIFFSetField(tif, TIFFTAG_COMPRESSION, compression);
        }
    }
    if (remaining >= 2) {
        uint16_t photometric = data[offset] | (data[offset+1] << 8);
        offset += 2;
        remaining -= 2;
        if (photometric == PHOTOMETRIC_MINISBLACK || photometric == PHOTOMETRIC_MINISWHITE ||
            photometric == PHOTOMETRIC_RGB || photometric == PHOTOMETRIC_PALETTE) {
            TIFFSetField(tif, TIFFTAG_PHOTOMETRIC, photometric);
        }
    }
    if (remaining >= 2) {
        uint16_t samples = data[offset] | (data[offset+1] << 8);
        offset += 2;
        remaining -= 2;
        if (samples >= 1 && samples <= 4) {
            TIFFSetField(tif, TIFFTAG_SAMPLESPERPIXEL, samples);
        }
    }
    if (remaining >= 2) {
        uint16_t bits = data[offset] | (data[offset+1] << 8);
        offset += 2;
        remaining -= 2;
        if (bits == 1 || bits == 8 || bits == 16 || bits == 32) {
            TIFFSetField(tif, TIFFTAG_BITSPERSAMPLE, bits);
        }
    }

    // Write scanlines using remaining data
    size_t scanline_size = TIFFScanlineSize(tif);
    if (scanline_size == 0) {
        TIFFClose(tif);
        unlink(filename);
        return 0;
    }

    uint8_t *buf = (uint8_t *)malloc(scanline_size);
    if (!buf) {
        TIFFClose(tif);
        unlink(filename);
        return 0;
    }

    for (uint32_t row = 0; row < height; row++) {
        memset(buf, 0, scanline_size);
        if (remaining > 0) {
            size_t copy = remaining < scanline_size ? remaining : scanline_size;
            memcpy(buf, data + offset, copy);
            offset += copy;
            remaining -= copy;
        }
        if (TIFFWriteScanline(tif, buf, row, 0) < 0) {
            break;
        }
    }

    free(buf);
    TIFFClose(tif);
    unlink(filename);
    return 0;
}