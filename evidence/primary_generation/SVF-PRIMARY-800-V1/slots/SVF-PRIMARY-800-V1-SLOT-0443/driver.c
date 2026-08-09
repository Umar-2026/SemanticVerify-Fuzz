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
    if (write(fd, data, size) != (ssize_t)size) {
        close(fd);
        unlink(filename);
        return 0;
    }
    close(fd);

    TIFF *tif = TIFFOpen(filename, "r");
    if (!tif) {
        unlink(filename);
        return 0;
    }

    // Process all directories in the TIFF file
    do {
        uint32_t w = 0, h = 0;
        uint16_t bits_per_sample = 1;
        uint16_t samples_per_pixel = 1;
        uint16_t photometric = PHOTOMETRIC_MINISBLACK;
        uint16_t planar_config = PLANARCONFIG_CONTIG;
        uint32_t rows_per_strip = 0;
        uint32_t strip_size = 0;
        uint32_t n_strips = 0;

        // Read common tags
        TIFFGetField(tif, TIFFTAG_IMAGEWIDTH, &w);
        TIFFGetField(tif, TIFFTAG_IMAGELENGTH, &h);
        TIFFGetField(tif, TIFFTAG_BITSPERSAMPLE, &bits_per_sample);
        TIFFGetField(tif, TIFFTAG_SAMPLESPERPIXEL, &samples_per_pixel);
        TIFFGetField(tif, TIFFTAG_PHOTOMETRIC, &photometric);
        TIFFGetField(tif, TIFFTAG_PLANARCONFIG, &planar_config);
        TIFFGetField(tif, TIFFTAG_ROWSPERSTRIP, &rows_per_strip);

        // Compute strip information
        if (w > 0 && h > 0 && rows_per_strip > 0) {
            strip_size = TIFFStripSize(tif);
            n_strips = TIFFNumberOfStrips(tif);
        }

        // Read strip data if available
        if (strip_size > 0 && n_strips > 0 && strip_size <= 1024 * 1024) {
            uint8_t *buf = (uint8_t *)malloc(strip_size);
            if (buf) {
                for (uint32_t strip = 0; strip < n_strips; strip++) {
                    tmsize_t read_size = TIFFReadEncodedStrip(tif, strip, buf, strip_size);
                    if (read_size < 0) break;
                }
                free(buf);
            }
        }

        // Read scanline data if dimensions are reasonable
        if (w > 0 && h > 0 && w <= 4096 && h <= 4096) {
            tmsize_t scanline_size = TIFFScanlineSize(tif);
            if (scanline_size > 0 && scanline_size <= 1024 * 1024) {
                uint8_t *buf = (uint8_t *)malloc(scanline_size);
                if (buf) {
                    for (uint32_t row = 0; row < h; row++) {
                        if (TIFFReadScanline(tif, buf, row, 0) < 0) break;
                    }
                    free(buf);
                }
            }
        }

        // Read tile data if tiled
        if (TIFFIsTiled(tif)) {
            uint32_t tw = 0, th = 0;
            TIFFGetField(tif, TIFFTAG_TILEWIDTH, &tw);
            TIFFGetField(tif, TIFFTAG_TILELENGTH, &th);
            if (tw > 0 && th > 0 && tw <= 4096 && th <= 4096) {
                tmsize_t tile_size = TIFFTileSize(tif);
                if (tile_size > 0 && tile_size <= 1024 * 1024) {
                    uint8_t *buf = (uint8_t *)malloc(tile_size);
                    if (buf) {
                        uint32_t n_tiles = TIFFNumberOfTiles(tif);
                        for (uint32_t tile = 0; tile < n_tiles; tile++) {
                            if (TIFFReadEncodedTile(tif, tile, buf, tile_size) < 0) break;
                        }
                        free(buf);
                    }
                }
            }
        }

        // Advance to next directory
    } while (TIFFReadDirectory(tif));

    TIFFClose(tif);
    unlink(filename);
    return 0;
}