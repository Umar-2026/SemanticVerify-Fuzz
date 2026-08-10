#include <lcms2.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 4) return 0;

    cmsHPROFILE input_profile = cmsOpenProfileFromMem(data, size);
    if (!input_profile) return 0;

    cmsHPROFILE output_profile = cmsCreate_sRGBProfile();
    if (!output_profile) {
        cmsCloseProfile(input_profile);
        return 0;
    }

    cmsUInt32Number input_format = TYPE_RGBA_8;
    cmsUInt32Number output_format = TYPE_RGBA_8;
    cmsUInt32Number intent = INTENT_PERCEPTUAL;
    cmsUInt32Number flags = cmsFLAGS_NOCACHE | cmsFLAGS_NOOPTIMIZE;

    cmsHTRANSFORM transform = cmsCreateTransform(input_profile, input_format,
                                                 output_profile, output_format,
                                                 intent, flags);
    if (!transform) {
        cmsCloseProfile(output_profile);
        cmsCloseProfile(input_profile);
        return 0;
    }

    // Representative pixel data: 16 pixels of RGBA, each channel 0..255
    uint8_t pixels[64];
    for (int i = 0; i < 64; i++) {
        pixels[i] = (uint8_t)(i * 4); // deterministic pattern
    }

    cmsDoTransform(transform, pixels, pixels, 16);

    cmsDeleteTransform(transform);
    cmsCloseProfile(output_profile);
    cmsCloseProfile(input_profile);
    return 0;
}