#include "lcms2.h"
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

#define MAX_INPUT_SIZE 4096

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 8 || size > MAX_INPUT_SIZE) {
        return 0;
    }

    // Extract bounded parameters from the first bytes
    uint32_t intent = data[0] % 4;          // 0..3
    uint32_t input_format = data[1] % 8;    // 0..7
    uint32_t output_format = data[2] % 8;   // 0..7
    uint32_t flags = data[3] & 0x03;        // 0..3
    uint32_t pixel_count = (data[4] << 8) | data[5];
    if (pixel_count == 0) {
        pixel_count = 1;
    }
    if (pixel_count > 256) {
        pixel_count = 256;
    }

    // Define format combinations based on bounded choices
    uint32_t in_fmt = 0;
    uint32_t out_fmt = 0;

    // Input format selection
    switch (input_format) {
        case 0: in_fmt = TYPE_GRAY_8; break;
        case 1: in_fmt = TYPE_GRAY_16; break;
        case 2: in_fmt = TYPE_RGB_8; break;
        case 3: in_fmt = TYPE_RGB_16; break;
        case 4: in_fmt = TYPE_CMYK_8; break;
        case 5: in_fmt = TYPE_CMYK_16; break;
        case 6: in_fmt = TYPE_Lab_8; break;
        default: in_fmt = TYPE_Lab_16; break;
    }

    // Output format selection
    switch (output_format) {
        case 0: out_fmt = TYPE_GRAY_8; break;
        case 1: out_fmt = TYPE_GRAY_16; break;
        case 2: out_fmt = TYPE_RGB_8; break;
        case 3: out_fmt = TYPE_RGB_16; break;
        case 4: out_fmt = TYPE_CMYK_8; break;
        case 5: out_fmt = TYPE_CMYK_16; break;
        case 6: out_fmt = TYPE_Lab_8; break;
        default: out_fmt = TYPE_Lab_16; break;
    }

    // Determine input pixel size in bytes
    size_t in_pixel_size = 0;
    switch (in_fmt) {
        case TYPE_GRAY_8: in_pixel_size = 1; break;
        case TYPE_GRAY_16: in_pixel_size = 2; break;
        case TYPE_RGB_8: in_pixel_size = 3; break;
        case TYPE_RGB_16: in_pixel_size = 6; break;
        case TYPE_CMYK_8: in_pixel_size = 4; break;
        case TYPE_CMYK_16: in_pixel_size = 8; break;
        case TYPE_Lab_8: in_pixel_size = 3; break;
        case TYPE_Lab_16: in_pixel_size = 6; break;
        default: return 0;
    }

    // Determine output pixel size in bytes
    size_t out_pixel_size = 0;
    switch (out_fmt) {
        case TYPE_GRAY_8: out_pixel_size = 1; break;
        case TYPE_GRAY_16: out_pixel_size = 2; break;
        case TYPE_RGB_8: out_pixel_size = 3; break;
        case TYPE_RGB_16: out_pixel_size = 6; break;
        case TYPE_CMYK_8: out_pixel_size = 4; break;
        case TYPE_CMYK_16: out_pixel_size = 8; break;
        case TYPE_Lab_8: out_pixel_size = 3; break;
        case TYPE_Lab_16: out_pixel_size = 6; break;
        default: return 0;
    }

    // Compute available input data size after header
    size_t available = size - 8;
    size_t needed = in_pixel_size * pixel_count;
    if (needed > available) {
        pixel_count = (uint32_t)(available / in_pixel_size);
        if (pixel_count == 0) {
            return 0;
        }
        needed = in_pixel_size * pixel_count;
    }

    // Allocate input and output buffers
    uint8_t *input = (uint8_t *)malloc(needed);
    uint8_t *output = (uint8_t *)malloc(out_pixel_size * pixel_count);
    if (!input || !output) {
        free(input);
        free(output);
        return 0;
    }

    // Copy input data from fuzz input
    memcpy(input, data + 8, needed);

    // Create profiles (use sRGB as input and Lab as output for simplicity)
    cmsHPROFILE hIn = cmsCreate_sRGBProfile();
    cmsHPROFILE hOut = cmsCreateLab4Profile(NULL);
    if (!hIn || !hOut) {
        if (hIn) cmsCloseProfile(hIn);
        if (hOut) cmsCloseProfile(hOut);
        free(input);
        free(output);
        return 0;
    }

    // Create transform
    cmsHTRANSFORM hTransform = cmsCreateTransform(hIn, in_fmt, hOut, out_fmt, intent, flags);
    if (!hTransform) {
        cmsCloseProfile(hIn);
        cmsCloseProfile(hOut);
        free(input);
        free(output);
        return 0;
    }

    // Perform transform
    cmsDoTransform(hTransform, input, output, pixel_count);

    // Cleanup
    cmsDeleteTransform(hTransform);
    cmsCloseProfile(hIn);
    cmsCloseProfile(hOut);
    free(input);
    free(output);

    return 0;
}