#include "lcms2.h"
#include <stdint.h>
#include <string.h>
#include <stdlib.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

    // Split input into two halves for profile data and transform parameters
    size_t half = size / 2;
    const uint8_t *profile_data = data;
    size_t profile_size = half;
    const uint8_t *transform_data = data + half;
    size_t transform_size = size - half;

    // Create profile from memory
    cmsHPROFILE profile = cmsOpenProfileFromMem(profile_data, profile_size);
    if (!profile) {
        // Profile creation failed, try with the other half
        profile = cmsOpenProfileFromMem(transform_data, transform_size);
        if (!profile) {
            return 0;
        }
    }

    // Create a second profile from the remaining data (if any)
    cmsHPROFILE profile2 = NULL;
    if (profile_size > 0 && transform_size > 0) {
        // Use the other half as a second profile
        profile2 = cmsOpenProfileFromMem(transform_data, transform_size);
        if (!profile2) {
            // If second profile fails, use the first profile as both input and output
            profile2 = profile;
        }
    } else {
        profile2 = profile;
    }

    // Determine transform parameters from the input data
    cmsUInt32Number input_format = 0;
    cmsUInt32Number output_format = 0;
    cmsUInt32Number intent = 0;
    cmsUInt32Number flags = 0;

    // Use bytes from transform_data to derive parameters
    if (transform_size >= 4) {
        input_format = (cmsUInt32Number)transform_data[0] | ((cmsUInt32Number)transform_data[1] << 8) |
                       ((cmsUInt32Number)transform_data[2] << 16) | ((cmsUInt32Number)transform_data[3] << 24);
        // Mask to valid format bits (e.g., TYPE_RGB_8, TYPE_RGBA_8, etc.)
        input_format &= 0x7FFFFFFF; // Clear sign bit
    }
    if (transform_size >= 8) {
        output_format = (cmsUInt32Number)transform_data[4] | ((cmsUInt32Number)transform_data[5] << 8) |
                        ((cmsUInt32Number)transform_data[6] << 16) | ((cmsUInt32Number)transform_data[7] << 24);
        output_format &= 0x7FFFFFFF;
    }
    if (transform_size >= 9) {
        intent = transform_data[8] % 4; // 0..3
    }
    if (transform_size >= 10) {
        flags = (cmsUInt32Number)transform_data[9] & 0x0000FFFF;
    }

    // Create transform
    cmsHTRANSFORM transform = cmsCreateTransform(profile, input_format, profile2, output_format, intent, flags);
    if (!transform) {
        // If transform creation fails, try with default formats
        transform = cmsCreateTransform(profile, TYPE_RGB_8, profile2, TYPE_RGB_8, INTENT_PERCEPTUAL, 0);
        if (!transform) {
            // Cleanup and return
            if (profile2 != profile) {
                cmsCloseProfile(profile2);
            }
            cmsCloseProfile(profile);
            return 0;
        }
    }

    // Apply transform to some dummy data if possible
    // Use a small buffer of bytes from the input
    unsigned char input_buffer[64];
    unsigned char output_buffer[64];
    size_t copy_size = transform_size < 64 ? transform_size : 64;
    if (copy_size > 0) {
        memcpy(input_buffer, transform_data, copy_size);
        // Zero-pad if needed
        if (copy_size < 64) {
            memset(input_buffer + copy_size, 0, 64 - copy_size);
        }
        // Determine number of pixels based on format (simplified: assume 3 bytes per pixel for RGB)
        cmsUInt32Number pixels = (cmsUInt32Number)(copy_size / 3);
        if (pixels > 0) {
            cmsDoTransform(transform, input_buffer, output_buffer, pixels);
        }
    }

    // Cleanup
    cmsDeleteTransform(transform);
    if (profile2 != profile) {
        cmsCloseProfile(profile2);
    }
    cmsCloseProfile(profile);

    return 0;
}