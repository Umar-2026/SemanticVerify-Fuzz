#include "lcms2.h"
#include <stdint.h>
#include <stdlib.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 64) return 0;

    cmsHPROFILE hInput = cmsCreate_sRGBProfile();
    cmsHPROFILE hOutput = cmsCreate_sRGBProfile();
    if (!hInput || !hOutput) {
        if (hInput) cmsCloseProfile(hInput);
        if (hOutput) cmsCloseProfile(hOutput);
        return 0;
    }

    cmsHTRANSFORM hTransform = cmsCreateTransform(hInput, TYPE_RGBA_8, hOutput, TYPE_RGBA_8, INTENT_PERCEPTUAL, 0);
    cmsCloseProfile(hInput);
    cmsCloseProfile(hOutput);

    if (!hTransform) return 0;

    size_t pixel_size = 4;
    size_t num_blocks = size / (pixel_size * 4);
    
    if (num_blocks > 0) {
        uint8_t *output_buffer = (uint8_t *)malloc(num_blocks * pixel_size * 4);
        if (output_buffer) {
            cmsDoTransform(hTransform, data, output_buffer, (cmsUInt32Number)(num_blocks * 4));
            free(output_buffer);
        }
    }

    cmsDeleteTransform(hTransform);
    return 0;
}