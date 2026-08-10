#include "lcms2.h"
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 4) return 0;

    cmsHPROFILE src_profile = NULL;
    cmsHPROFILE dst_profile = NULL;
    cmsHTRANSFORM transform = NULL;
    cmsToneCurve *curve = NULL;
    cmsUInt16Number *input_buffer = NULL;
    cmsUInt16Number *output_buffer = NULL;

    // Extract gamma value from first 4 bytes (as float)
    float gamma;
    memcpy(&gamma, data, sizeof(gamma));
    if (gamma < 0.1f || gamma > 10.0f) gamma = 2.2f;

    // Create tone curve from fuzz-derived gamma
    curve = cmsBuildGamma(NULL, gamma);
    if (!curve) goto cleanup;

    // Create a simple RGB profile with the tone curve as TRC
    cmsToneCurve *curves[3] = {curve, curve, curve};
    src_profile = cmsCreateRGBProfile(cmsD50_xyY(), cmsD50_xyY(), curves);
    if (!src_profile) goto cleanup;

    // Create a Lab profile as destination
    dst_profile = cmsCreateLab4Profile(NULL);
    if (!dst_profile) goto cleanup;

    // Create transform from RGB to Lab
    transform = cmsCreateTransform(src_profile, TYPE_RGB_16, dst_profile, TYPE_Lab_16,
                                   INTENT_PERCEPTUAL, 0);
    if (!transform) goto cleanup;

    // Allocate buffers
    size_t pixel_count = (size - 4) / 6; // 3 channels * 2 bytes each
    if (pixel_count == 0) goto cleanup;
    if (pixel_count > 1024) pixel_count = 1024;

    input_buffer = (cmsUInt16Number *)malloc(pixel_count * 3 * sizeof(cmsUInt16Number));
    output_buffer = (cmsUInt16Number *)malloc(pixel_count * 3 * sizeof(cmsUInt16Number));
    if (!input_buffer || !output_buffer) goto cleanup;

    // Fill input buffer from fuzz data (after gamma bytes)
    size_t offset = 4;
    for (size_t i = 0; i < pixel_count * 3; i++) {
        if (offset + 2 <= size) {
            input_buffer[i] = (cmsUInt16Number)((data[offset] << 8) | data[offset + 1]);
            offset += 2;
        } else {
            input_buffer[i] = 0;
        }
    }

    // Apply transform
    cmsDoTransform(transform, input_buffer, output_buffer, pixel_count);

cleanup:
    if (transform) cmsDeleteTransform(transform);
    if (src_profile) cmsCloseProfile(src_profile);
    if (dst_profile) cmsCloseProfile(dst_profile);
    if (curve) cmsFreeToneCurve(curve);
    free(input_buffer);
    free(output_buffer);

    return 0;
}