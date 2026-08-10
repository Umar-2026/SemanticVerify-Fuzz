#include "lcms2.h"
#include <stdint.h>
#include <stdlib.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1024) {
        return 0;
    }

    cmsHPROFILE hInput = cmsCreate_sRGBProfile();
    cmsHPROFILE hOutput = cmsCreate_sRGBProfile();

    if (!hInput || !hOutput) {
        if (hInput) cmsCloseProfile(hInput);
        if (hOutput) cmsCloseProfile(hOutput);
        return 0;
    }

    cmsHTRANSFORM hTransform = cmsCreateTransform(
        hInput, TYPE_RGBA_8,
        hOutput, TYPE_RGBA_8,
        INTENT_PERCEPTUAL, 0
    );

    if (hTransform) {
        size_t pixel_count = (size - 512) / 4;
        if (pixel_count > 0) {
            uint8_t *output_buffer = (uint8_t *)malloc(pixel_count * 4);
            if (output_buffer) {
                cmsDoTransform(hTransform, data + 512, output_buffer, (cmsUInt32Number)pixel_count);
                free(output_buffer);
            }
        }
        cmsDeleteTransform(hTransform);
    }

    cmsCloseProfile(hInput);
    cmsCloseProfile(hOutput);

    return 0;
}