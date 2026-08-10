#include "lcms2.h"
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

    cmsHPROFILE profile = cmsCreateProfilePlaceholder(0);
    if (!profile) return 0;

    cmsToneCurve *curve = NULL;
    cmsToneCurve *curve_dup = NULL;
    cmsHPROFILE linear_profile = NULL;
    cmsHTRANSFORM transform = NULL;

    // Use first byte to derive gamma value (avoid zero and extreme values)
    uint16_t gamma_val = (uint16_t)(data[0] | (data[1] << 8));
    double gamma = 1.0 + (double)(gamma_val % 1000) / 100.0; // 1.0 to 10.99

    // Create tone curve using required symbol
    curve = cmsBuildGamma(0, gamma);
    if (!curve) goto cleanup;

    // Duplicate curve for potential use
    curve_dup = cmsDupToneCurve(curve);
    if (!curve_dup) goto cleanup;

    // Create a linear RGB profile
    linear_profile = cmsCreateRGBProfile(cmsD50_xyY(), 
                                         &(cmsCIExyY){0.6400, 0.3300, 1.0},
                                         &(cmsCIExyY){0.3000, 0.6000, 1.0},
                                         &(cmsCIExyY){0.1500, 0.0600, 1.0});
    if (!linear_profile) goto cleanup;

    // Set the tone curve as TRC for the gray profile? Instead, create a gray profile and set TRC
    cmsHPROFILE gray_profile = cmsCreateGrayProfile(cmsD50_xyY(), curve);
    if (!gray_profile) goto cleanup;

    // Create a transform from gray to linear RGB using the curve
    transform = cmsCreateTransform(gray_profile, TYPE_GRAY_8, linear_profile, TYPE_RGB_8, 
                                   INTENT_PERCEPTUAL, 0);
    if (!transform) goto cleanup;

    // Use the transform with fuzz data
    size_t n_pixels = size > 2 ? (size - 2) : 0;
    if (n_pixels > 1024) n_pixels = 1024;
    if (n_pixels > 0) {
        uint8_t *input = (uint8_t *)data + 2;
        uint8_t output[1024 * 3];
        cmsDoTransform(transform, input, output, n_pixels);
    }

    // Also test curve evaluation directly
    if (size > 2) {
        double in_val = (double)(data[2] % 256) / 255.0;
        double out_val = cmsEvalToneCurveFloat(curve, (float)in_val);
        (void)out_val;
    }

cleanup:
    if (transform) cmsDeleteTransform(transform);
    if (gray_profile) cmsCloseProfile(gray_profile);
    if (linear_profile) cmsCloseProfile(linear_profile);
    if (curve_dup) cmsFreeToneCurve(curve_dup);
    if (curve) cmsFreeToneCurve(curve);
    if (profile) cmsCloseProfile(profile);
    return 0;
}