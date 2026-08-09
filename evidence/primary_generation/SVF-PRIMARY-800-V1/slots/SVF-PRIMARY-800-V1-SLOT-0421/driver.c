#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <tiffio.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

    // Create a temporary file to hold the fuzz data
    char filename[] = "/tmp/libtiff_fuzz_XXXXXX";
    int fd = mkstemp(filename);
    if (fd < 0) return 0;
    ssize_t written = write(fd, data, size);
    close(fd);
    if (written != (ssize_t)size) {
        unlink(filename);
        return 0;
    }

    TIFF *tif = TIFFOpen(filename, "r");
    if (tif) {
        uint32_t width = 0, height = 0;
        uint16_t bits_per_sample = 0, samples_per_pixel = 0;
        uint16_t photometric = 0;
        uint32_t tile_width = 0, tile_length = 0;
        uint16_t planar_config = 0;

        TIFFGetField(tif, TIFFTAG_IMAGEWIDTH, &width);
        TIFFGetField(tif, TIFFTAG_IMAGELENGTH, &height);
        TIFFGetField(tif, TIFFTAG_BITSPERSAMPLE, &bits_per_sample);
        TIFFGetField(tif, TIFFTAG_SAMPLESPERPIXEL, &samples_per_pixel);
        TIFFGetField(tif, TIFFTAG_PHOTOMETRIC, &photometric);
        TIFFGetField(tif, TIFFTAG_PLANARCONFIG, &planar_config);

        // Attempt to read scanline data if dimensions are sane
        if (width > 0 && height > 0 && width <= 65536 && height <= 65536) {
            tmsize_t scanline_size = TIFFScanlineSize(tif);
            if (scanline_size > 0 && scanline_size <= (tmsize_t)(size * 2 + 1024)) {
                uint8_t *buf = (uint8_t *)malloc((size_t)scanline_size);
                if (buf) {
                    for (uint32_t row = 0; row < height; row++) {
                        if (TIFFReadScanline(tif, buf, row, 0) < 0) {
                            break;
                        }
                    }
                    free(buf);
                }
            }
        }

        // Attempt to read tile data if tiled
        if (TIFFIsTiled(tif)) {
            TIFFGetField(tif, TIFFTAG_TILEWIDTH, &tile_width);
            TIFFGetField(tif, TIFFTAG_TILELENGTH, &tile_length);
            if (tile_width > 0 && tile_length > 0 && tile_width <= 65536 && tile_length <= 65536) {
                tmsize_t tile_size = TIFFTileSize(tif);
                if (tile_size > 0 && tile_size <= (tmsize_t)(size * 2 + 1024)) {
                    uint8_t *tile_buf = (uint8_t *)malloc((size_t)tile_size);
                    if (tile_buf) {
                        uint32_t tiles_across = (width + tile_width - 1) / tile_width;
                        uint32_t tiles_down = (height + tile_length - 1) / tile_length;
                        for (uint32_t ty = 0; ty < tiles_down; ty++) {
                            for (uint32_t tx = 0; tx < tiles_across; tx++) {
                                if (TIFFReadTile(tif, tile_buf, tx * tile_width, ty * tile_length, 0, 0) < 0) {
                                    break;
                                }
                            }
                        }
                        free(tile_buf);
                    }
                }
            }
        }

        TIFFClose(tif);
    }

    unlink(filename);
    return 0;
}