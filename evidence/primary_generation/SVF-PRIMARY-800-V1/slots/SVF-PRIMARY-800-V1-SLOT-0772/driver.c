#include <stdint.h>
#include <stddef.h>
#include "lcms2.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 64) {
        return 0;
    }

    cmsHPROFILE hInput = cmsOpenProfileFromMem(data, size / 2);
    if (!hInput) {
        return 0;
    }

    cmsHPROFILE hOutput = cmsOpenProfileFromMem(data + (size / 2), size / 2);
    if (!hOutput) {
        cmsCloseProfile(hInput);
        return 0;
    }

    cmsHTRANSFORM hTransform = cmsCreateTransform(
        hInput, TYPE_RGBA_8,
        hOutput, TYPE_RGBA_8,
        INTENT_PERCEPTUAL, 0
    );

    if (hTransform) {
        uint8_t output_buffer[4];
        cmsDoTransform(hTransform, data, output_buffer, 1);
        cmsDeleteTransform(hTransform);
    }

    cmsCloseProfile(hInput);
    cmsCloseProfile(hOutput);

    return 0;
}