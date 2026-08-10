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

    cmsUInt32Number input_format = TYPE_RGB_8;
    cmsUInt32Number output_format = TYPE_RGB_8;
    cmsUInt32Number intent = INTENT_PERCEPTUAL;
    cmsUInt32Number flags = cmsFLAGS_NOCACHE | cmsFLAGS_NOOPTIMIZE;

    cmsHTRANSFORM transform = cmsCreateTransform(input_profile, input_format,
                                                 output_profile, output_format,
                                                 intent, flags);
    if (!transform) {
        cmsCloseProfile(input_profile);
        cmsCloseProfile(output_profile);
        return 0;
    }

    // Representative pixel data: 64x64 RGB image
    const int width = 64;
    const int height = 64;
    size_t pixel_count = (size_t)width * height;
    size_t input_size = pixel_count * 3;
    size_t output_size = pixel_count * 3;

    uint8_t *input_pixels = (uint8_t *)malloc(input_size);
    uint8_t *output_pixels = (uint8_t *)malloc(output_size);
    if (!input_pixels || !output_pixels) {
        free(input_pixels);
        free(output_pixels);
        cmsDeleteTransform(transform);
        cmsCloseProfile(input_profile);
        cmsCloseProfile(output_profile);
        return 0;
    }

    // Fill with deterministic gradient pattern derived from input data
    for (size_t i = 0; i < pixel_count; i++) {
        input_pixels[i * 3 + 0] = (uint8_t)((data[i % size] + i) & 0xFF);
        input_pixels[i * 3 + 1] = (uint8_t)((data[(i + 1) % size] + i * 2) & 0xFF);
        input_pixels[i * 3 + 2] = (uint8_t)((data[(i + 2) % size] + i * 3) & 0xFF);
    }

    cmsDoTransform(transform, input_pixels, output_pixels, (cmsUInt32Number)pixel_count);

    free(input_pixels);
    free(output_pixels);
    cmsDeleteTransform(transform);
    cmsCloseProfile(input_profile);
    cmsCloseProfile(output_profile);

    return 0;
}