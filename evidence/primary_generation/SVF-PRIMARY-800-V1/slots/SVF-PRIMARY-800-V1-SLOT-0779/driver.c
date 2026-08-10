#include "lcms2.h"
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 8) return 0;

    // Split input into two profiles and pixel data
    size_t half = size / 2;
    const uint8_t *input_profile_data = data;
    size_t input_profile_size = half;
    const uint8_t *output_profile_data = data + half;
    size_t output_profile_size = size - half;

    // Ensure at least some pixel data (at least 4 bytes for one pixel)
    if (output_profile_size < 4) return 0;

    // Create input profile from memory
    cmsHPROFILE input_profile = cmsOpenProfileFromMem(input_profile_data, input_profile_size);
    if (!input_profile) return 0;

    // Create output profile from memory
    cmsHPROFILE output_profile = cmsOpenProfileFromMem(output_profile_data, output_profile_size);
    if (!output_profile) {
        cmsCloseProfile(input_profile);
        return 0;
    }

    // Create transform from input to output in 32-bit float format
    cmsHTRANSFORM transform = cmsCreateTransform(input_profile, TYPE_RGBA_FLT,
                                                 output_profile, TYPE_RGBA_FLT,
                                                 INTENT_PERCEPTUAL, 0);
    if (!transform) {
        cmsCloseProfile(input_profile);
        cmsCloseProfile(output_profile);
        return 0;
    }

    // Determine number of pixels from remaining data (after profiles)
    // We have output_profile_size bytes for output profile, but we need pixel data.
    // Recompute: total size = input_profile_size + output_profile_size + pixel_data_size
    // We allocated half for input, rest for output, but we need pixel data too.
    // Let's re-split: use first quarter for input, second quarter for output, rest for pixels.
    // But we already split. Instead, use the tail of output_profile_data as pixel data.
    // To keep it simple, we'll use the last 4 bytes of the whole input as one pixel.
    // But we need at least 4 bytes for pixel. We already checked output_profile_size >= 4.
    // Use the last 4 bytes of the entire data as pixel data.
    if (size < 12) { // need at least 4 bytes for input, 4 for output, 4 for pixel
        cmsCloseProfile(input_profile);
        cmsCloseProfile(output_profile);
        cmsDeleteTransform(transform);
        return 0;
    }

    // Re-split: first 1/3 for input, second 1/3 for output, last 1/3 for pixels
    size_t third = size / 3;
    if (third < 4) {
        cmsCloseProfile(input_profile);
        cmsCloseProfile(output_profile);
        cmsDeleteTransform(transform);
        return 0;
    }

    // Close previous profiles and transform, reopen with new split
    cmsDeleteTransform(transform);
    cmsCloseProfile(input_profile);
    cmsCloseProfile(output_profile);

    input_profile = cmsOpenProfileFromMem(data, third);
    if (!input_profile) return 0;
    output_profile = cmsOpenProfileFromMem(data + third, third);
    if (!output_profile) {
        cmsCloseProfile(input_profile);
        return 0;
    }

    transform = cmsCreateTransform(input_profile, TYPE_RGBA_FLT,
                                   output_profile, TYPE_RGBA_FLT,
                                   INTENT_PERCEPTUAL, 0);
    if (!transform) {
        cmsCloseProfile(input_profile);
        cmsCloseProfile(output_profile);
        return 0;
    }

    // Pixel data is the remaining bytes after the two profiles
    const uint8_t *pixel_data = data + 2 * third;
    size_t pixel_data_size = size - 2 * third;
    if (pixel_data_size < 4) {
        cmsDeleteTransform(transform);
        cmsCloseProfile(input_profile);
        cmsCloseProfile(output_profile);
        return 0;
    }

    // Number of pixels we can process: each pixel is 4 floats (RGBA) = 16 bytes
    // But we have raw bytes; we'll interpret them as float array.
    size_t num_pixels = pixel_data_size / 16;
    if (num_pixels == 0) {
        cmsDeleteTransform(transform);
        cmsCloseProfile(input_profile);
        cmsCloseProfile(output_profile);
        return 0;
    }

    // Allocate input and output buffers
    float *input_pixels = (float *)malloc(num_pixels * 4 * sizeof(float));
    float *output_pixels = (float *)malloc(num_pixels * 4 * sizeof(float));
    if (!input_pixels || !output_pixels) {
        free(input_pixels);
        free(output_pixels);
        cmsDeleteTransform(transform);
        cmsCloseProfile(input_profile);
        cmsCloseProfile(output_profile);
        return 0;
    }

    // Copy pixel data into input buffer (interpret bytes as floats)
    memcpy(input_pixels, pixel_data, num_pixels * 4 * sizeof(float));

    // Perform the transform
    cmsDoTransform(transform, input_pixels, output_pixels, num_pixels);

    // Clean up
    free(input_pixels);
    free(output_pixels);
    cmsDeleteTransform(transform);
    cmsCloseProfile(input_profile);
    cmsCloseProfile(output_profile);

    return 0;
}