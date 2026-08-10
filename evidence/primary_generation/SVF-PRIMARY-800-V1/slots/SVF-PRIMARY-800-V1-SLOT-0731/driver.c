#include <lcms2.h>
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

    // Use first 16 bytes for parameters
    if (size >= 16) {
        memcpy(&input_format, data, 4);
        memcpy(&output_format, data + 4, 4);
        memcpy(&n_pixels, data + 8, 4);
        memcpy(&flags, data + 12, 4);
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
    if (n_pixels == 0 || n_pixels > 1024) n_pixels = 1;

    // Determine input and output pixel sizes based on formats
    size_t input_pixel_size = 0;
    size_t output_pixel_size = 0;

    // Simple mapping for common formats; for unknown, default to 3 bytes
    switch (input_format) {
        case TYPE_GRAY_8: input_pixel_size = 1; break;
        case TYPE_GRAY_16: input_pixel_size = 2; break;
        case TYPE_RGB_8: input_pixel_size = 3; break;
        case TYPE_RGB_16: input_pixel_size = 6; break;
        case TYPE_RGBA_8: input_pixel_size = 4; break;
        case TYPE_RGBA_16: input_pixel_size = 8; break;
        case TYPE_CMYK_8: input_pixel_size = 4; break;
        case TYPE_CMYK_16: input_pixel_size = 8; break;
        default: input_pixel_size = 3; break;
    }

    switch (output_format) {
        case TYPE_GRAY_8: output_pixel_size = 1; break;
        case TYPE_GRAY_16: output_pixel_size = 2; break;
        case TYPE_RGB_8: output_pixel_size = 3; break;
        case TYPE_RGB_16: output_pixel_size = 6; break;
        case TYPE_RGBA_8: output_pixel_size = 4; break;
        case TYPE_RGBA_16: output_pixel_size = 8; break;
        case TYPE_CMYK_8: output_pixel_size = 4; break;
        case TYPE_CMYK_16: output_pixel_size = 8; break;
        default: output_pixel_size = 3; break;
    }

    // Ensure we have enough input data for at least one pixel
    size_t needed_input = input_pixel_size * n_pixels;
    if (size < needed_input) {
        // Use what we have, but at least one pixel
        n_pixels = size / input_pixel_size;
        if (n_pixels == 0) n_pixels = 1;
        needed_input = input_pixel_size * n_pixels;
        if (size < needed_input) {
            // Not enough for even one pixel, pad with zeros
            // We'll allocate and copy
        }
    }

    // Allocate input buffer (pad with zeros if needed)
    uint8_t *input_buffer = (uint8_t *)malloc(needed_input);
    if (!input_buffer) return 0;
    if (size >= needed_input) {
        memcpy(input_buffer, data, needed_input);
    } else {
        memcpy(input_buffer, data, size);
        memset(input_buffer + size, 0, needed_input - size);
    }

    // Allocate output buffer
    size_t output_size = output_pixel_size * n_pixels;
    uint8_t *output_buffer = (uint8_t *)malloc(output_size);
    if (!output_buffer) {
        free(input_buffer);
        return 0;
    }

    // Create a transform using sRGB profiles
    cmsHPROFILE input_profile = cmsCreate_sRGBProfile();
    cmsHPROFILE output_profile = cmsCreate_sRGBProfile();
    if (!input_profile || !output_profile) {
        if (input_profile) cmsCloseProfile(input_profile);
        if (output_profile) cmsCloseProfile(output_profile);
        free(input_buffer);
        free(output_buffer);
        return 0;
    }

    cmsHTRANSFORM transform = cmsCreateTransform(
        input_profile, input_format,
        output_profile, output_format,
        cmsGetProfileID(input_profile), flags
    );

    cmsCloseProfile(input_profile);
    cmsCloseProfile(output_profile);

    if (!transform) {
        free(input_buffer);
        free(output_buffer);
        return 0;
    }

    // Process the pixel blocks
    cmsDoTransform(transform, input_buffer, output_buffer, n_pixels);

    // Cleanup
    cmsDeleteTransform(transform);
    free(input_buffer);
    free(output_buffer);

    return 0;
}