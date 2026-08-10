#include <stdint.h>
#include <stddef.h>
#include "lcms2.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 128) {
        return 0;
    }

    cmsHPROFILE hProfile = cmsOpenProfileFromMem(data, size);
    if (hProfile == NULL) {
        return 0;
    }

    cmsHTRANSFORM hTransform = cmsCreateTransform(
        hProfile,
        TYPE_RGB_8,
        hProfile,
        TYPE_RGB_8,
        INTENT_PERCEPTUAL,
        cmsFLAGS_NOCACHE
    );

    if (hTransform != NULL) {
        uint8_t input[3] = {128, 128, 128};
        uint8_t output[3] = {0, 0, 0};
        cmsDoTransform(hTransform, input, output, 1);
        cmsDeleteTransform(hTransform);
    } else {
        cmsUInt32Number version = cmsGetProfileVersion(hProfile);
        (void)version;
    }

    cmsCloseProfile(hProfile);

    return 0;
}