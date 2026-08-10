#include "lcms2.h"
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1024) {
        return 0;
    }

    cmsHPROFILE hInput = cmsOpenProfileFromMem(data, 512);
    if (!hInput) {
        return 0;
    }

    cmsHPROFILE hOutput = cmsOpenProfileFromMem(data + 512, 512);
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
        size_t remaining = size - 1024;
        size_t numPixels = remaining / 4;
        if (numPixels > 0) {
            uint8_t *outputBuffer = malloc(numPixels * 4);
            if (outputBuffer) {
                cmsDoTransform(hTransform, data + 1024, outputBuffer, (cmsUInt32Number)numPixels);
                free(outputBuffer);
            }
        }
        cmsDeleteTransform(hTransform);
    }

    cmsCloseProfile(hInput);
    cmsCloseProfile(hOutput);

    return 0;
}