#include "lcms2.h"
#include <stdint.h>
#include <stdlib.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 128) {
        return 0;
    }

    cmsHPROFILE hInputProfile = cmsCreate_sRGBProfile();
    cmsHPROFILE hOutputProfile = cmsCreate_sRGBProfile();

    if (!hInputProfile || !hOutputProfile) {
        if (hInputProfile) cmsCloseProfile(hInputProfile);
        if (hOutputProfile) cmsCloseProfile(hOutputProfile);
        return 0;
    }

    cmsHTRANSFORM hTransform = cmsCreateTransform(
        hInputProfile, TYPE_RGBA_8,
        hOutputProfile, TYPE_RGBA_8,
        INTENT_PERCEPTUAL, 0
    );

    if (hTransform) {
        size_t pixel_count = size / 4;
        if (pixel_count > 0) {
            uint8_t *output = (uint8_t *)malloc(pixel_count * 4);
            if (output) {
                cmsDoTransform(hTransform, data, output, (cmsUInt32Number)pixel_count);
                free(output);
            }
        }
        cmsDeleteTransform(hTransform);
    }

    cmsCloseProfile(hInputProfile);
    cmsCloseProfile(hOutputProfile);

    return 0;
}