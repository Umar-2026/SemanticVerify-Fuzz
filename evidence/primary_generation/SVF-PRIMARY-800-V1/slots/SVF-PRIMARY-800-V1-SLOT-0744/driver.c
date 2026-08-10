#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include "lcms2.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 12) {
        return 0;
    }

    cmsHPROFILE hInput = cmsCreate_sRGBProfile();
    cmsHPROFILE hOutput = cmsCreate_sRGBProfile();
    
    cmsHTRANSFORM hTransform = cmsCreateTransform(
        hInput, TYPE_RGB_8,
        hOutput, TYPE_RGB_8,
        INTENT_PERCEPTUAL, 0
    );

    if (!hTransform) {
        cmsCloseProfile(hInput);
        cmsCloseProfile(hOutput);
        return 0;
    }

    size_t half = size / 2;
    uint8_t *buffer1 = (uint8_t *)malloc(half);
    uint8_t *buffer2 = (uint8_t *)malloc(size - half);
    uint8_t *out1 = (uint8_t *)malloc(half);
    uint8_t *out2 = (uint8_t *)malloc(size - half);

    if (buffer1 && buffer2 && out1 && out2) {
        memcpy(buffer1, data, half);
        memcpy(buffer2, data + half, size - half);

        cmsDoTransform(hTransform, buffer1, out1, (cmsUInt32Number)(half / 3));
        cmsDoTransform(hTransform, buffer2, out2, (cmsUInt32Number)((size - half) / 3));
    }

    free(buffer1);
    free(buffer2);
    free(out1);
    free(out2);

    cmsDeleteTransform(hTransform);
    cmsCloseProfile(hInput);
    cmsCloseProfile(hOutput);

    return 0;
}