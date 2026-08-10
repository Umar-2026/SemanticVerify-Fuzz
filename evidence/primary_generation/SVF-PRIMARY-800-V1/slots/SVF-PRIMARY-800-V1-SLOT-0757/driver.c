#include "lcms2.h"
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1) return 0;

    // Extract a gamma value from the first byte (avoid 0 and extreme values)
    double gamma = (double)(data[0] % 200 + 1) / 100.0; // 0.01 to 2.00

    // Build a tone curve using cmsBuildGamma
    cmsToneCurve *curve = cmsBuildGamma(NULL, gamma);
    if (!curve) return 0;

    // Create a profile and attach the curve as a tone reproduction curve
    cmsHPROFILE profile = cmsCreateProfilePlaceholder(NULL);
    if (!profile) {
        cmsFreeToneCurve(curve);
        return 0;
    }

    // Set the tone curve as the TRC for the gray profile (or use as input)
    cmsSetProfileVersion(profile, 4.3);
    cmsSetDeviceClass(profile, cmsSigDisplayClass);
    cmsSetColorSpace(profile, cmsSigGrayData);
    cmsSetPCS(profile, cmsSigGrayData);

    // Attach the curve to the profile's gray TRC tag
    cmsWriteTag(profile, cmsSigGrayTRCTag, curve);

    // Create a transform from the profile to itself (or to a standard space)
    cmsHPROFILE lab_profile = cmsCreateLab4Profile(NULL);
    if (!lab_profile) {
        cmsCloseProfile(profile);
        cmsFreeToneCurve(curve);
        return 0;
    }

    cmsHTRANSFORM transform = cmsCreateTransform(profile, TYPE_GRAY_8, lab_profile, TYPE_Lab_DBL, INTENT_PERCEPTUAL, 0);
    if (transform) {
        // Use a small portion of the input data as pixel values
        size_t pixel_count = size > 1 ? (size - 1) : 0;
        if (pixel_count > 256) pixel_count = 256;
        uint8_t *gray_pixels = (uint8_t *)malloc(pixel_count);
        if (gray_pixels) {
            for (size_t i = 0; i < pixel_count; i++) {
                gray_pixels[i] = data[1 + i % (size - 1)];
            }
            // Allocate output buffer for Lab values (3 doubles per pixel)
            double *lab_out = (double *)malloc(pixel_count * 3 * sizeof(double));
            if (lab_out) {
                cmsDoTransform(transform, gray_pixels, lab_out, pixel_count);
                free(lab_out);
            }
            free(gray_pixels);
        }
        cmsDeleteTransform(transform);
    }

    // Cleanup
    cmsCloseProfile(lab_profile);
    cmsCloseProfile(profile);
    cmsFreeToneCurve(curve);

    return 0;
}