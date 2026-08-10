#include "lcms2.h"
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 8) return 0;

    // Split input into two profiles and pixel data
    size_t half = size / 2;
    const uint8_t *profile1_data = data;
    size_t profile1_size = half;
    const uint8_t *profile2_data = data + half;
    size_t profile2_size = size - half;

    // Ensure at least some pixel data remains (use last 64 bytes for pixels)
    if (profile2_size < 64) return 0;
    size_t pixel_size = 64;
    profile2_size -= pixel_size;
    const uint8_t *pixel_data = profile2_data + profile2_size;

    // Open profiles from memory
    cmsHPROFILE hIn = cmsOpenProfileFromMem(profile1_data, profile1_size);
    if (!hIn) return 0;
    cmsHPROFILE hOut = cmsOpenProfileFromMem(profile2_data, profile2_size);
    if (!hOut) {
        cmsCloseProfile(hIn);
        return 0;
    }

    // Create transform with fuzz-derived input/output formats
    // Use 4-channel float input and output (RGBA)
    cmsUInt32Number inputFormat = TYPE_RGBA_FLT;
    cmsUInt32Number outputFormat = TYPE_RGBA_FLT;
    cmsUInt32Number intent = INTENT_PERCEPTUAL;
    cmsUInt32Number flags = cmsFLAGS_NOCACHE | cmsFLAGS_NOOPTIMIZE;

    cmsHTRANSFORM hTransform = cmsCreateTransform(hIn, inputFormat, hOut, outputFormat, intent, flags);
    cmsCloseProfile(hIn);
    cmsCloseProfile(hOut);
    if (!hTransform) return 0;

    // Process pixel data: 64 bytes = 4 pixels of 4 floats (16 bytes each)
    // Copy to aligned buffer to avoid alignment issues
    float pixels_in[16];
    float pixels_out[16];
    memcpy(pixels_in, pixel_data, pixel_size);

    cmsDoTransform(hTransform, pixels_in, pixels_out, 4);

    // Consume output to prevent optimization
    volatile float sink = 0;
    for (int i = 0; i < 16; i++) {
        sink += pixels_out[i];
    }
    (void)sink;

    cmsDeleteTransform(hTransform);
    return 0;
}