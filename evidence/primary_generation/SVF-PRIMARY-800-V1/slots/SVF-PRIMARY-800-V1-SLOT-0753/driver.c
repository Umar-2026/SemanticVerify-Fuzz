#include "lcms2.h"
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1) return 0;

    // Extract gamma value from first byte (0-255 -> 0.0 to 25.5)
    double gamma = (double)(data[0] & 0xFF) / 10.0;
    if (gamma < 0.01) gamma = 0.01;

    // Build tone curve using fuzz-derived gamma
    cmsToneCurve *curve = cmsBuildGamma(NULL, gamma);
    if (!curve) return 0;

    // Create a profile and attach the curve as a tone reproduction curve
    cmsHPROFILE profile = cmsCreateProfilePlaceholder(NULL);
    if (!profile) {
        cmsFreeToneCurve(curve);
        return 0;
    }

    // Set the tone curve as the TRC for the gray profile (simple usage)
    cmsSetProfileTRC(profile, cmsSigGrayTRCTag, curve);

    // Create a transform from the profile to sRGB to exercise the curve
    cmsHPROFILE srgb = cmsCreate_sRGBProfile();
    if (!srgb) {
        cmsCloseProfile(profile);
        cmsFreeToneCurve(curve);
        return 0;
    }

    cmsHTRANSFORM transform = cmsCreateTransform(profile, TYPE_GRAY_8, srgb, TYPE_RGB_8, INTENT_PERCEPTUAL, 0);
    if (transform) {
        // Use remaining bytes as pixel data (if any)
        size_t pixel_count = (size - 1) / 3; // 3 bytes per RGB pixel
        if (pixel_count > 0) {
            uint8_t *gray_pixels = (uint8_t *)malloc(pixel_count);
            uint8_t *rgb_pixels = (uint8_t *)malloc(pixel_count * 3);
            if (gray_pixels && rgb_pixels) {
                // Fill gray pixels from input data (skip first byte)
                for (size_t i = 0; i < pixel_count; i++) {
                    gray_pixels[i] = data[1 + (i % (size - 1))];
                }
                cmsDoTransform(transform, gray_pixels, rgb_pixels, pixel_count);
            }
            free(gray_pixels);
            free(rgb_pixels);
        }
        cmsDeleteTransform(transform);
    }

    cmsCloseProfile(srgb);
    cmsCloseProfile(profile);
    cmsFreeToneCurve(curve);

    return 0;
}