#include <lcms2.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) {
        return 0;
    }

    cmsHPROFILE profile = cmsOpenProfileFromMem(data, size);
    if (profile) {
        cmsHTRANSFORM transform = cmsCreateTransform(profile, TYPE_RGB_8, profile, TYPE_RGB_8, INTENT_PERCEPTUAL, 0);
        if (transform) {
            uint8_t input[3] = {0x10, 0x20, 0x30};
            uint8_t output[3] = {0};
            cmsDoTransform(transform, input, output, 1);
            cmsDeleteTransform(transform);
        }
        cmsCloseProfile(profile);
        return 1;
    }

    return 0;
}