#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <tiffio.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 8) return 0;

    // Create a temporary file to hold the input data
    char filename[] = "/tmp/libtiff_fuzz_XXXXXX";
    int fd = mkstemp(filename);
    if (fd < 0) return 0;
    write(fd, data, size);
    close(fd);

    TIFF *tif = TIFFOpen(filename, "r");
    if (!tif) {
        unlink(filename);
        return 0;
    }

    // Process all directories in the file
    do {
        // Read basic information from the current directory
        uint32_t width, height;
        uint16_t bits_per_sample, samples_per_pixel;
        uint16_t photometric;

        TIFFGetField(tif, TIFFTAG_IMAGEWIDTH, &width);
        TIFFGetField(tif, TIFFTAG_IMAGELENGTH, &height);
        TIFFGetField(tif, TIFFTAG_BITSPERSAMPLE, &bits_per_sample);
        TIFFGetField(tif, TIFFTAG_SAMPLESPERPIXEL, &samples_per_pixel);
        TIFFGetField(tif, TIFFTAG_PHOTOMETRIC, &photometric);

        // Attempt to read the image data if dimensions are reasonable
        if (width > 0 && height > 0 && width < 10000 && height < 10000) {
            tmsize_t scanline_size = TIFFScanlineSize(tif);
            if (scanline_size > 0 && scanline_size < 1000000) {
                unsigned char *buf = (unsigned char *)malloc(scanline_size);
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

        // Also try to read the directory as a strip-based image
        tmsize_t strip_size = TIFFStripSize(tif);
        if (strip_size > 0 && strip_size < 1000000) {
            unsigned char *strip_buf = (unsigned char *)malloc(strip_size);
            if (strip_buf) {
                tstrip_t num_strips = TIFFNumberOfStrips(tif);
                for (tstrip_t s = 0; s < num_strips; s++) {
                    if (TIFFReadEncodedStrip(tif, s, strip_buf, strip_size) < 0) {
                        break;
                    }
                }
                free(strip_buf);
            }
        }

        // Try to read the directory as a tile-based image
        uint32_t tile_width, tile_length;
        TIFFGetField(tif, TIFFTAG_TILEWIDTH, &tile_width);
        TIFFGetField(tif, TIFFTAG_TILELENGTH, &tile_length);
        if (tile_width > 0 && tile_length > 0) {
            tmsize_t tile_size = TIFFTileSize(tif);
            if (tile_size > 0 && tile_size < 1000000) {
                unsigned char *tile_buf = (unsigned char *)malloc(tile_size);
                if (tile_buf) {
                    ttile_t num_tiles = TIFFNumberOfTiles(tif);
                    for (ttile_t t = 0; t < num_tiles; t++) {
                        if (TIFFReadEncodedTile(tif, t, tile_buf, tile_size) < 0) {
                            break;
                        }
                    }
                    free(tile_buf);
                }
            }
        }

    } while (TIFFReadDirectory(tif));

    TIFFClose(tif);
    unlink(filename);
    return 0;
}