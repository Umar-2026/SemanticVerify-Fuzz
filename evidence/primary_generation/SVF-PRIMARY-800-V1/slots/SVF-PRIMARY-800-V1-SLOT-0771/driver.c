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

    // Determine number of pixels from remaining data (use up to 1024 pixels)
    size_t available = size - half; // This is output_profile_size, but we need pixel data after profiles
    // Actually, we used all data for profiles, so we need to extract pixel data from the profile data itself.
    // To keep it simple, we'll use a fixed small buffer derived from the input data.
    // Use the first 16 bytes of the input as pixel data (4 pixels of RGBA float)
    float pixels[16];
    for (int i = 0; i < 16 && i < (int)size; i++) {
        pixels[i] = (float)data[i] / 255.0f;
    }
    // Fill remaining with zeros if needed
    for (int i = (int)size; i < 16; i++) {
        pixels[i] = 0.0f;
    }

    // Process 4 pixels (16 floats)
    float output_pixels[16];
    cmsDoTransform(transform, pixels, output_pixels, 4);

    // Clean up
    cmsDeleteTransform(transform);
    cmsCloseProfile(input_profile);
    cmsCloseProfile(output_profile);

    return 0;
}