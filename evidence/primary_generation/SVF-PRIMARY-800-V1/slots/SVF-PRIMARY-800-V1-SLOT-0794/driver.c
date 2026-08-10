#include <stdint.h>
#include <stddef.h>
#include "lcms2.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 128) {
        return 0;
    }

    cmsHPROFILE hInputProfile = cmsOpenProfileFromMem(data, size);
    if (!hInputProfile) {
        return 0;
    }

    cmsHPROFILE hOutputProfile = cmsCreate_sRGBProfile();
    if (!hOutputProfile) {
        cmsCloseProfile(hInputProfile);
        return 0;
    }

    cmsHTRANSFORM hTransform = cmsCreateTransform(
        hInputProfile,
        TYPE_RGB_8,
        hOutputProfile,
        TYPE_RGB_8,
        INTENT_PERCEPTUAL,
        0
    );

    if (hTransform) {
        uint8_t inputPixel[3] = {128, 64, 32};
        uint8_t outputPixel[3] = {0, 0, 0};

        cmsDoTransform(hTransform, inputPixel, outputPixel, 1);

        cmsDeleteTransform(hTransform);
    }

    cmsCloseProfile(hInputProfile);
    cmsCloseProfile(hOutputProfile);

    return 0;
}