#include <lcms2.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

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

    // Create transform from input to output in Lab color space
    cmsHTRANSFORM transform = cmsCreateTransform(input_profile, TYPE_Lab_DBL,
                                                 output_profile, TYPE_Lab_DBL,
                                                 INTENT_PERCEPTUAL, 0);
    if (!transform) {
        cmsCloseProfile(input_profile);
        cmsCloseProfile(output_profile);
        return 0;
    }

    // Determine number of pixels from remaining data (we use all data for profiles, so use fixed small size)
    // Since we used all data for profiles, generate pixel data deterministically from input
    // Use a small fixed number of pixels to avoid excessive memory usage
    const int num_pixels = 16;
    double input_pixels[num_pixels * 3];
    double output_pixels[num_pixels * 3];

    // Fill input pixels with fuzz-derived values (use bytes from input profile data as seed)
    for (int i = 0; i < num_pixels * 3; i++) {
        uint8_t byte = input_profile_data[i % input_profile_size];
        input_pixels[i] = (double)(byte) / 255.0 * 100.0; // Lab L range 0-100
        // For a and b, map to -128..127
        if (i % 3 != 0) {
            input_pixels[i] = (double)(byte) - 128.0;
        }
    }

    // Perform transform
    cmsDoTransform(transform, input_pixels, output_pixels, num_pixels);

    // Clean up
    cmsDeleteTransform(transform);
    cmsCloseProfile(input_profile);
    cmsCloseProfile(output_profile);

    return 0;
}