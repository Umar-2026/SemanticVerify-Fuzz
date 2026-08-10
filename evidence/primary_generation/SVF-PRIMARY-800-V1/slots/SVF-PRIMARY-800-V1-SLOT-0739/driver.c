#include "lcms2.h"
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 8) return 0;

    // Extract parameters from fuzz input
    uint32_t input_format = 0;
    uint32_t output_format = 0;
    uint32_t n_pixels = 0;
    uint32_t flags = 0;

    // Use first 16 bytes for parameters (little-endian)
    if (size >= 16) {
        input_format = (uint32_t)data[0] | ((uint32_t)data[1] << 8) | ((uint32_t)data[2] << 16) | ((uint32_t)data[3] << 24);
        output_format = (uint32_t)data[4] | ((uint32_t)data[5] << 8) | ((uint32_t)data[6] << 16) | ((uint32_t)data[7] << 24);
        n_pixels = (uint32_t)data[8] | ((uint32_t)data[9] << 8) | ((uint32_t)data[10] << 16) | ((uint32_t)data[11] << 24);
        flags = (uint32_t)data[12] | ((uint32_t)data[13] << 8) | ((uint32_t)data[14] << 16) | ((uint32_t)data[15] << 24);
        data += 16;
        size -= 16;
    } else {
        // Fallback defaults
        input_format = TYPE_RGB_8;
        output_format = TYPE_RGB_8;
        n_pixels = 1;
        flags = 0;
    }

    // Limit n_pixels to avoid excessive memory usage
    if (n_pixels > 1024) n_pixels = 1024;

    // Determine bytes per pixel based on format (simplified: assume max 16 bytes per pixel)
    size_t max_pixel_size = 16;
    size_t needed = (size_t)n_pixels * max_pixel_size;
    if (size < needed) {
        // Not enough data, adjust n_pixels
        n_pixels = (uint32_t)(size / max_pixel_size);
        if (n_pixels == 0) return 0;
    }

    // Create a simple sRGB profile for input and output
    cmsHPROFILE hIn = cmsCreate_sRGBProfile();
    cmsHPROFILE hOut = cmsCreate_sRGBProfile();
    if (!hIn || !hOut) {
        if (hIn) cmsCloseProfile(hIn);
        if (hOut) cmsCloseProfile(hOut);
        return 0;
    }

    // Create transform
    cmsHTRANSFORM hTransform = cmsCreateTransform(hIn, input_format, hOut, output_format, INTENT_PERCEPTUAL, flags);
    if (!hTransform) {
        cmsCloseProfile(hIn);
        cmsCloseProfile(hOut);
        return 0;
    }

    // Prepare input buffer (copy fuzz data, zero-pad if needed)
    size_t input_size = (size_t)n_pixels * max_pixel_size;
    uint8_t *input_buffer = (uint8_t *)malloc(input_size);
    if (!input_buffer) {
        cmsDeleteTransform(hTransform);
        cmsCloseProfile(hIn);
        cmsCloseProfile(hOut);
        return 0;
    }
    memset(input_buffer, 0, input_size);
    memcpy(input_buffer, data, size < input_size ? size : input_size);

    // Prepare output buffer
    uint8_t *output_buffer = (uint8_t *)malloc(input_size);
    if (!output_buffer) {
        free(input_buffer);
        cmsDeleteTransform(hTransform);
        cmsCloseProfile(hIn);
        cmsCloseProfile(hOut);
        return 0;
    }
    memset(output_buffer, 0, input_size);

    // Perform transform on the pixel block
    cmsDoTransform(hTransform, input_buffer, output_buffer, n_pixels);

    // Cleanup
    free(output_buffer);
    free(input_buffer);
    cmsDeleteTransform(hTransform);
    cmsCloseProfile(hIn);
    cmsCloseProfile(hOut);

    return 0;
}