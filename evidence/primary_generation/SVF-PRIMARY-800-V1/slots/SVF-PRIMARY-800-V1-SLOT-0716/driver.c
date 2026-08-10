#include "lcms2.h"
#include <stdint.h>
#include <stdlib.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 16) {
        return 0;
    }

    cmsHPROFILE hInput = cmsCreate_sRGBProfile();
    cmsHPROFILE hOutput = cmsCreate_sRGBProfile();

    if (!hInput || !hOutput) {
        if (hInput) cmsCloseProfile(hInput);
        if (hOutput) cmsCloseProfile(hOutput);
        return 0;
    }

    uint32_t intent = data[0] % 4;
    uint32_t inputFormat = TYPE_RGB_8;
    uint32_t outputFormat = TYPE_RGB_8;

    cmsHTRANSFORM hTransform = cmsCreateTransform(
        hInput, inputFormat,
        hOutput, outputFormat,
        intent, cmsFLAGS_NOCACHE
    );

    if (hTransform) {
        size_t pixelCount = (size - 1) / 3;
        if (pixelCount > 0) {
            uint8_t *outputBuffer = malloc(pixelCount * 3);
            if (outputBuffer) {
                cmsDoTransform(hTransform, &data[1], outputBuffer, (cmsUInt32Number)pixelCount);
                free(outputBuffer);
            }
        }
        cmsDeleteTransform(hTransform);
    }

    cmsCloseProfile(hInput);
    cmsCloseProfile(hOutput);

    return 0;
}