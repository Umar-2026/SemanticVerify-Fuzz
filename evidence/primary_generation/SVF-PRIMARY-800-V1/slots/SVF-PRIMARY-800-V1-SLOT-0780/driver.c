#include <stdint.h>
#include <stddef.h>
#include "lcms2.h"

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
        size_t pixels = remaining / 4;
        if (pixels > 0) {
            uint8_t *output_buffer = (uint8_t *)malloc(pixels * 4);
            if (output_buffer) {
                cmsDoTransform(hTransform, data + 1024, output_buffer, (cmsUInt32Number)pixels);
                free(output_buffer);
            }
        }
        cmsDeleteTransform(hTransform);
    }

    cmsCloseProfile(hInput);
    cmsCloseProfile(hOutput);

    return 0;
}