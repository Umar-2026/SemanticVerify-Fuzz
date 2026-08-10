#include "lcms2.h"
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 8) return 0;

    cmsHPROFILE hIn = cmsCreate_sRGBProfile();
    cmsHPROFILE hOut = cmsCreateLab4Profile(NULL);
    if (!hIn || !hOut) {
        if (hIn) cmsCloseProfile(hIn);
        if (hOut) cmsCloseProfile(hOut);
        return 0;
    }

    cmsHTRANSFORM hTransform = cmsCreateTransform(hIn, TYPE_RGB_8, hOut, TYPE_Lab_DBL, INTENT_PERCEPTUAL, 0);
    cmsCloseProfile(hIn);
    cmsCloseProfile(hOut);
    if (!hTransform) return 0;

    size_t half = size / 2;
    const uint8_t *data1 = data;
    const uint8_t *data2 = data + half;
    size_t size1 = half;
    size_t size2 = size - half;

    // Ensure each buffer has at least one full pixel (3 bytes)
    if (size1 < 3 || size2 < 3) {
        cmsDeleteTransform(hTransform);
        return 0;
    }

    // Limit number of pixels to avoid excessive memory usage
    size_t maxPixels = 1024;
    size_t pixels1 = size1 / 3;
    size_t pixels2 = size2 / 3;
    if (pixels1 > maxPixels) pixels1 = maxPixels;
    if (pixels2 > maxPixels) pixels2 = maxPixels;

    size_t bytes1 = pixels1 * 3;
    size_t bytes2 = pixels2 * 3;

    // Allocate output buffers for Lab double (3 doubles per pixel)
    size_t outSize1 = pixels1 * 3 * sizeof(double);
    size_t outSize2 = pixels2 * 3 * sizeof(double);
    double *out1 = (double *)malloc(outSize1);
    double *out2 = (double *)malloc(outSize2);
    if (!out1 || !out2) {
        free(out1);
        free(out2);
        cmsDeleteTransform(hTransform);
        return 0;
    }

    // Perform first transform
    cmsDoTransform(hTransform, (void *)data1, out1, (cmsUInt32Number)pixels1);

    // Perform second transform on the other buffer
    cmsDoTransform(hTransform, (void *)data2, out2, (cmsUInt32Number)pixels2);

    // Simple check to ensure outputs are finite (optional)
    for (size_t i = 0; i < pixels1 * 3; i++) {
        if (out1[i] != out1[i]) { // NaN check
            free(out1);
            free(out2);
            cmsDeleteTransform(hTransform);
            return 0;
        }
    }
    for (size_t i = 0; i < pixels2 * 3; i++) {
        if (out2[i] != out2[i]) {
            free(out1);
            free(out2);
            cmsDeleteTransform(hTransform);
            return 0;
        }
    }

    free(out1);
    free(out2);
    cmsDeleteTransform(hTransform);
    return 0;
}