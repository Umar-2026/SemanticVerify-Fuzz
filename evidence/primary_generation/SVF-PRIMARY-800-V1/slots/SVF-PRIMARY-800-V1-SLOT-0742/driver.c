#include <stdint.h>
#include <stdlib.h>
#include "lcms2.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 128) {
        return 0;
    }

    cmsHPROFILE hInput = cmsCreate_sRGBProfile();
    cmsHPROFILE hOutput = cmsCreate_sRGBProfile();
    
    if (!hInput || !hOutput) {
        if (hInput) cmsCloseProfile(hInput);
        if (hOutput) cmsCloseProfile(hOutput);
        return 0;
    }

    cmsHTRANSFORM hTransform = cmsCreateTransform(hInput, TYPE_RGB_8, hOutput, TYPE_RGB_8, INTENT_PERCEPTUAL, 0);
    
    if (!hTransform) {
        cmsCloseProfile(hInput);
        cmsCloseProfile(hOutput);
        return 0;
    }

    size_t half_size = (size - 64) / 2;
    uint8_t *out1 = malloc(half_size);
    uint8_t *out2 = malloc(half_size);

    if (out1 && out2) {
        cmsDoTransform(hTransform, data, out1, (cmsUInt32Number)(half_size / 3));
        cmsDoTransform(hTransform, data + half_size, out2, (cmsUInt32Number)(half_size / 3));
    }

    free(out1);
    free(out2);
    cmsDeleteTransform(hTransform);
    cmsCloseProfile(hInput);
    cmsCloseProfile(hOutput);

    return 0;
}