#include "lcms2.h"
#include <stdint.h>
#include <stdlib.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 64) return 0;

    cmsHPROFILE hInput = cmsCreate_sRGBProfile();
    cmsHPROFILE hOutput = cmsCreate_sRGBProfile();
    if (!hInput || !hOutput) {
        if (hInput) cmsCloseProfile(hInput);
        return 0;
    }

    cmsHTRANSFORM hTransform = cmsCreateTransform(hInput, TYPE_RGBA_8, hOutput, TYPE_RGBA_8, INTENT_PERCEPTUAL, 0);
    cmsCloseProfile(hInput);
    cmsCloseProfile(hOutput);

    if (!hTransform) return 0;

    size_t num_blocks = 4;
    size_t block_size = size / num_blocks;
    
    if (block_size >= 4) {
        uint8_t *output_buffer = malloc(block_size);
        if (output_buffer) {
            for (size_t i = 0; i < num_blocks; i++) {
                cmsDoTransform(hTransform, data + (i * block_size), output_buffer, block_size / 4);
            }
            free(output_buffer);
        }
    }

    cmsDeleteTransform(hTransform);
    return 0;
}