#include "lcms2.h"
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 8) return 0;

    cmsHPROFILE src_profile = cmsCreate_sRGBProfile();
    cmsHPROFILE dst_profile = cmsCreateLab4Profile(NULL);
    if (!src_profile || !dst_profile) {
        if (src_profile) cmsCloseProfile(src_profile);
        if (dst_profile) cmsCloseProfile(dst_profile);
        return 0;
    }

    cmsHTRANSFORM transform = cmsCreateTransform(src_profile, TYPE_RGB_8,
                                                 dst_profile, TYPE_Lab_DBL,
                                                 INTENT_PERCEPTUAL, 0);
    if (!transform) {
        cmsCloseProfile(src_profile);
        cmsCloseProfile(dst_profile);
        return 0;
    }

    size_t half = size / 2;
    const uint8_t *buf1 = data;
    const uint8_t *buf2 = data + half;
    size_t len1 = half;
    size_t len2 = size - half;

    size_t pixels1 = len1 / 3;
    size_t pixels2 = len2 / 3;
    if (pixels1 == 0 || pixels2 == 0) {
        cmsDeleteTransform(transform);
        cmsCloseProfile(src_profile);
        cmsCloseProfile(dst_profile);
        return 0;
    }

    size_t out_size1 = pixels1 * 3 * sizeof(double);
    size_t out_size2 = pixels2 * 3 * sizeof(double);
    double *out1 = (double *)malloc(out_size1);
    double *out2 = (double *)malloc(out_size2);
    if (!out1 || !out2) {
        free(out1);
        free(out2);
        cmsDeleteTransform(transform);
        cmsCloseProfile(src_profile);
        cmsCloseProfile(dst_profile);
        return 0;
    }

    cmsDoTransform(transform, buf1, out1, pixels1);
    cmsDoTransform(transform, buf2, out2, pixels2);

    free(out1);
    free(out2);
    cmsDeleteTransform(transform);
    cmsCloseProfile(src_profile);
    cmsCloseProfile(dst_profile);
    return 0;
}