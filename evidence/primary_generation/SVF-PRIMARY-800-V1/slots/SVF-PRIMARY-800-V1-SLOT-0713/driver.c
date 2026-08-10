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

    // Determine pixel size based on format (simplified: 3 or 4 channels, 8 or 16 bits)
    size_t input_pixel_size = 3 * sizeof(uint8_t);
    size_t output_pixel_size = 3 * sizeof(uint8_t);
    if (input_format >= 4) input_pixel_size = 4 * sizeof(uint8_t);
    if (output_format >= 4) output_pixel_size = 4 * sizeof(uint8_t);

    // Use remaining data as pixel data (at least one pixel)
    size_t pixel_data_size = size - 4;
    if (pixel_data_size < input_pixel_size) {
        return 0;
    }
    size_t num_pixels = pixel_data_size / input_pixel_size;
    if (num_pixels == 0) {
        return 0;
    }

    // Create a simple RGB profile (sRGB) for input and output
    cmsHPROFILE input_profile = cmsCreate_sRGBProfile();
    cmsHPROFILE output_profile = cmsCreate_sRGBProfile();
    if (!input_profile || !output_profile) {
        if (input_profile) cmsCloseProfile(input_profile);
        if (output_profile) cmsCloseProfile(output_profile);
        return 0;
    }

    // Map format index to cms formats
    cmsUInt32Number in_fmt, out_fmt;
    switch (input_format) {
        case 0: in_fmt = TYPE_RGB_8; break;
        case 1: in_fmt = TYPE_RGB_16; break;
        case 2: in_fmt = TYPE_RGBA_8; break;
        case 3: in_fmt = TYPE_RGBA_16; break;
        case 4: in_fmt = TYPE_RGB_8; break; // fallback
        case 5: in_fmt = TYPE_RGB_16; break;
        case 6: in_fmt = TYPE_RGBA_8; break;
        default: in_fmt = TYPE_RGBA_16; break;
    }
    switch (output_format) {
        case 0: out_fmt = TYPE_RGB_8; break;
        case 1: out_fmt = TYPE_RGB_16; break;
        case 2: out_fmt = TYPE_RGBA_8; break;
        case 3: out_fmt = TYPE_RGBA_16; break;
        case 4: out_fmt = TYPE_RGB_8; break;
        case 5: out_fmt = TYPE_RGB_16; break;
        case 6: out_fmt = TYPE_RGBA_8; break;
        default: out_fmt = TYPE_RGBA_16; break;
    }

    // Create transform
    cmsHTRANSFORM transform = cmsCreateTransform(
        input_profile, in_fmt,
        output_profile, out_fmt,
        intent, flags
    );
    if (!transform) {
        cmsCloseProfile(input_profile);
        cmsCloseProfile(output_profile);
        return 0;
    }

    // Prepare input buffer (copy from fuzz data)
    size_t input_buffer_size = num_pixels * input_pixel_size;
    uint8_t *input_buffer = (uint8_t *)malloc(input_buffer_size);
    if (!input_buffer) {
        cmsDeleteTransform(transform);
        cmsCloseProfile(input_profile);
        cmsCloseProfile(output_profile);
        return 0;
    }
    memcpy(input_buffer, data + 4, input_buffer_size);

    // Output buffer
    size_t output_buffer_size = num_pixels * output_pixel_size;
    uint8_t *output_buffer = (uint8_t *)malloc(output_buffer_size);
    if (!output_buffer) {
        free(input_buffer);
        cmsDeleteTransform(transform);
        cmsCloseProfile(input_profile);
        cmsCloseProfile(output_profile);
        return 0;
    }

    // Process pixels
    cmsDoTransform(transform, input_buffer, output_buffer, num_pixels);

    // Cleanup
    free(output_buffer);
    free(input_buffer);
    cmsDeleteTransform(transform);
    cmsCloseProfile(input_profile);
    cmsCloseProfile(output_profile);

    return 0;
}