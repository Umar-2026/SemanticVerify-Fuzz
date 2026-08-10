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

    cmsHTRANSFORM transform = cmsCreateTransform(input_profile, input_format,
                                                 output_profile, output_format,
                                                 INTENT_PERCEPTUAL, 0);
    if (!transform) {
        cmsCloseProfile(input_profile);
        cmsCloseProfile(output_profile);
        return 0;
    }

    // Representative pixel data: 16x16 RGBA image
    const int width = 16;
    const int height = 16;
    uint8_t pixels[width * height * 4];
    for (int i = 0; i < width * height * 4; i++) {
        pixels[i] = (uint8_t)(i * 7 + 3);
    }

    cmsDoTransform(transform, pixels, pixels, width * height);

    cmsDeleteTransform(transform);
    cmsCloseProfile(input_profile);
    cmsCloseProfile(output_profile);

    return 0;
}