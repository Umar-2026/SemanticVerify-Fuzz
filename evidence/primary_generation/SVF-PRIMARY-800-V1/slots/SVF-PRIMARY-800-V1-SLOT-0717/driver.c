#include "lcms2.h"
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

#define MAX_INPUT_SIZE 4096

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 8 || size > MAX_INPUT_SIZE) {
        return 0;
    }

    // Parse bounded parameters from the first bytes
    uint32_t intent = data[0] % 4; // 0..3
    uint32_t input_format = data[1] % 8; // 0..7
    uint32_t output_format = data[2] % 8; // 0..7
    uint32_t flags = data[3] & 0x03; // 0..3

    // Define format mappings (simplified)
    cmsUInt32Number in_fmt, out_fmt;
    switch (input_format) {
        case 0: in_fmt = TYPE_RGB_8; break;
        case 1: in_fmt = TYPE_RGB_16; break;
        case 2: in_fmt = TYPE_RGBA_8; break;
        case 3: in_fmt = TYPE_RGBA_16; break;
        case 4: in_fmt = TYPE_CMYK_8; break;
        case 5: in_fmt = TYPE_CMYK_16; break;
        case 6: in_fmt = TYPE_GRAY_8; break;
        default: in_fmt = TYPE_GRAY_16; break;
    }
    switch (output_format) {
        case 0: out_fmt = TYPE_RGB_8; break;
        case 1: out_fmt = TYPE_RGB_16; break;
        case 2: out_fmt = TYPE_RGBA_8; break;
        case 3: out_fmt = TYPE_RGBA_16; break;
        case 4: out_fmt = TYPE_CMYK_8; break;
        case 5: out_fmt = TYPE_CMYK_16; break;
        case 6: out_fmt = TYPE_GRAY_8; break;
        default: out_fmt = TYPE_GRAY_16; break;
    }

    // Create a simple sRGB profile for input and output
    cmsHPROFILE hIn = cmsCreate_sRGBProfile();
    if (!hIn) {
        return 0;
    }
    cmsHPROFILE hOut = cmsCreate_sRGBProfile();
    if (!hOut) {
        cmsCloseProfile(hIn);
        return 0;
    }

    // Create transform
    cmsHTRANSFORM hTransform = cmsCreateTransform(hIn, in_fmt, hOut, out_fmt, intent, flags);
    cmsCloseProfile(hIn);
    cmsCloseProfile(hOut);
    if (!hTransform) {
        return 0;
    }

    // Determine number of pixels from remaining data (at least 1 pixel)
    size_t pixel_size_in = cmsFormatterForColorspace(cmsGetColorSpace(hIn), in_fmt, 0) ? 0 : 0; // not used
    // Compute input pixel size based on format
    size_t in_pixel_size;
    switch (in_fmt) {
        case TYPE_RGB_8: in_pixel_size = 3; break;
        case TYPE_RGB_16: in_pixel_size = 6; break;
        case TYPE_RGBA_8: in_pixel_size = 4; break;
        case TYPE_RGBA_16: in_pixel_size = 8; break;
        case TYPE_CMYK_8: in_pixel_size = 4; break;
        case TYPE_CMYK_16: in_pixel_size = 8; break;
        case TYPE_GRAY_8: in_pixel_size = 1; break;
        default: in_pixel_size = 2; break;
    }
    size_t out_pixel_size;
    switch (out_fmt) {
        case TYPE_RGB_8: out_pixel_size = 3; break;
        case TYPE_RGB_16: out_pixel_size = 6; break;
        case TYPE_RGBA_8: out_pixel_size = 4; break;
        case TYPE_RGBA_16: out_pixel_size = 8; break;
        case TYPE_CMYK_8: out_pixel_size = 4; break;
        case TYPE_CMYK_16: out_pixel_size = 8; break;
        case TYPE_GRAY_8: out_pixel_size = 1; break;
        default: out_pixel_size = 2; break;
    }

    size_t available = size - 4;
    size_t max_pixels = available / in_pixel_size;
    if (max_pixels == 0) {
        cmsDeleteTransform(hTransform);
        return 0;
    }
    size_t num_pixels = max_pixels < 1024 ? max_pixels : 1024; // limit to 1024 pixels

    // Allocate input and output buffers
    size_t in_bytes = num_pixels * in_pixel_size;
    size_t out_bytes = num_pixels * out_pixel_size;
    uint8_t *in_buf = (uint8_t *)malloc(in_bytes);
    uint8_t *out_buf = (uint8_t *)malloc(out_bytes);
    if (!in_buf || !out_buf) {
        free(in_buf);
        free(out_buf);
        cmsDeleteTransform(hTransform);
        return 0;
    }

    // Copy pixel data from fuzz input
    memcpy(in_buf, data + 4, in_bytes);

    // Perform transform
    cmsDoTransform(hTransform, in_buf, out_buf, (cmsUInt32Number)num_pixels);

    // Cleanup
    free(in_buf);
    free(out_buf);
    cmsDeleteTransform(hTransform);

    return 0;
}