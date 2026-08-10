#include "lcms2.h"
#include <stdint.h>
#include <stdlib.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 64) return 0;

    cmsHPROFILE hInput = cmsCreate_sRGBProfile();
    cmsHPROFILE hOutput = cmsCreate_sRGBProfile();
    if (!hInput || !hOutput) return 0;

    cmsHTRANSFORM hTransform = cmsCreateTransform(hInput, TYPE_RGBA_8, hOutput, TYPE_RGBA_8, INTENT_PERCEPTUAL, 0);
    if (!hTransform) {
        cmsCloseProfile(hInput);
        cmsCloseProfile(hOutput);
        return 0;
    }

    size_t offset = 0;
    size_t blockSize = 16;
    uint8_t outputBuffer[16];

    while (offset + blockSize <= size) {
        cmsDoTransform(hTransform, data + offset, outputBuffer, 4);
        offset += blockSize;
    }

    cmsDeleteTransform(hTransform);
    cmsCloseProfile(hInput);
    cmsCloseProfile(hOutput);

    return 0;
}