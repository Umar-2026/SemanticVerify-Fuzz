#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <tiffio.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

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
        // Access basic directory information
        uint32_t width = 0, height = 0;
        uint16_t bits_per_sample = 0, samples_per_pixel = 0;
        uint16_t compression = 0, photometric = 0;

        TIFFGetField(tif, TIFFTAG_IMAGEWIDTH, &width);
        TIFFGetField(tif, TIFFTAG_IMAGELENGTH, &height);
        TIFFGetField(tif, TIFFTAG_BITSPERSAMPLE, &bits_per_sample);
        TIFFGetField(tif, TIFFTAG_SAMPLESPERPIXEL, &samples_per_pixel);
        TIFFGetField(tif, TIFFTAG_COMPRESSION, &compression);
        TIFFGetField(tif, TIFFTAG_PHOTOMETRIC, &photometric);

        // If dimensions are valid, attempt to read scanlines
        if (width > 0 && height > 0 && width <= 65536 && height <= 65536) {
            tmsize_t scanline_size = TIFFScanlineSize(tif);
            if (scanline_size > 0 && scanline_size <= (tmsize_t)size) {
                uint8_t *buf = (uint8_t *)malloc(scanline_size);
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

        // Attempt to read the directory's strip/tile info
        uint32_t strips_per_image = 0;
        if (TIFFGetField(tif, TIFFTAG_STRIPBYTECOUNTS, &strips_per_image) == 0) {
            // Not a strip-based image, try tile-based
            uint32_t tiles_per_image = 0;
            if (TIFFGetField(tif, TIFFTAG_TILEBYTECOUNTS, &tiles_per_image) == 0) {
                // No strip or tile info, just continue
            }
        }

        // Move to the next directory if it exists
    } while (TIFFReadDirectory(tif));

    TIFFClose(tif);
    unlink(filename);
    return 0;
}