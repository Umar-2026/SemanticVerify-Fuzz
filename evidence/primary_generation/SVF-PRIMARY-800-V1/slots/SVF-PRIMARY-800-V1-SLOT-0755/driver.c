#include "lcms2.h"
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1) return 0;

    // Use first byte to derive gamma value (avoid zero and negative)
    double gamma = (double)(data[0] % 100 + 1) / 10.0; // 0.1 to 10.0

    // Build tone curve from fuzz-derived gamma
    cmsToneCurve *curve = cmsBuildGamma(NULL, gamma);
    if (!curve) return 0;

    // Create a profile with the tone curve as TRC for gray
    cmsHPROFILE profile = cmsCreateGrayProfile(cmsD50_xyY(), curve);
    if (!profile) {
        cmsFreeToneCurve(curve);
        return 0;
    }

    // Create a transform from profile to sRGB
    cmsHPROFILE srgb = cmsCreate_sRGBProfile();
    if (!srgb) {
        cmsCloseProfile(profile);
        cmsFreeToneCurve(curve);
        return 0;
    }

    cmsHTRANSFORM transform = cmsCreateTransform(profile, TYPE_GRAY_8, srgb, TYPE_RGB_8, INTENT_PERCEPTUAL, 0);
    if (!transform) {
        cmsCloseProfile(srgb);
        cmsCloseProfile(profile);
        cmsFreeToneCurve(curve);
        return 0;
    }

    // Process a small buffer if enough data
    if (size > 1) {
        size_t n = size - 1;
        if (n > 256) n = 256;
        uint8_t gray[256];
        uint8_t rgb[256 * 3];
        for (size_t i = 0; i < n; i++) {
            gray[i] = data[1 + i];
        }
        cmsDoTransform(transform, gray, rgb, n);
    }

    // Cleanup
    cmsDeleteTransform(transform);
    cmsCloseProfile(srgb);
    cmsCloseProfile(profile);
    cmsFreeToneCurve(curve);

    return 0;
}