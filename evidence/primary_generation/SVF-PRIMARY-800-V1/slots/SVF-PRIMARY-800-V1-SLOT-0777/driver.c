#include <lcms2.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

#define MAX_PROFILE_SIZE 1024 * 1024
#define MAX_PIXELS 4096

static cmsHPROFILE load_profile(const uint8_t *data, size_t size) {
    if (size == 0 || size > MAX_PROFILE_SIZE) return NULL;
    cmsHPROFILE h = cmsOpenProfileFromMem(data, size);
    return h;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

    // Split input into two profiles and pixel data
    size_t half = size / 2;
    const uint8_t *profile1_data = data;
    size_t profile1_size = half;
    const uint8_t *profile2_data = data + half;
    size_t profile2_size = size - half;

    // Ensure at least some pixel data remains
    if (profile2_size < 4) return 0;

    // Extract pixel count from last 2 bytes of second profile section
    size_t pixel_bytes = (profile2_size >= 2) ? (profile2_data[profile2_size - 2] << 8 | profile2_data[profile2_size - 1]) : 0;
    pixel_bytes = pixel_bytes % MAX_PIXELS;
    if (pixel_bytes == 0) pixel_bytes = 1;

    // Reduce profile2 size to leave room for pixel data
    if (profile2_size <= pixel_bytes + 2) return 0;
    profile2_size -= pixel_bytes + 2;

    cmsHPROFILE hIn = load_profile(profile1_data, profile1_size);
    cmsHPROFILE hOut = load_profile(profile2_data, profile2_size);

    if (!hIn || !hOut) {
        if (hIn) cmsCloseProfile(hIn);
        if (hOut) cmsCloseProfile(hOut);
        return 0;
    }

    // Determine input and output formats based on profile color spaces
    cmsColorSpaceSignature inSpace = cmsGetColorSpace(hIn);
    cmsColorSpaceSignature outSpace = cmsGetColorSpace(hOut);

    uint32_t inFormat, outFormat;
    int inChannels, outChannels;

    switch (inSpace) {
        case cmsSigRgbData:
            inFormat = TYPE_RGB_8;
            inChannels = 3;
            break;
        case cmsSigGrayData:
            inFormat = TYPE_GRAY_8;
            inChannels = 1;
            break;
        case cmsSigCmykData:
            inFormat = TYPE_CMYK_8;
            inChannels = 4;
            break;
        case cmsSigLabData:
            inFormat = TYPE_Lab_8;
            inChannels = 3;
            break;
        default:
            inFormat = TYPE_RGB_8;
            inChannels = 3;
            break;
    }

    switch (outSpace) {
        case cmsSigRgbData:
            outFormat = TYPE_RGB_8;
            outChannels = 3;
            break;
        case cmsSigGrayData:
            outFormat = TYPE_GRAY_8;
            outChannels = 1;
            break;
        case cmsSigCmykData:
            outFormat = TYPE_CMYK_8;
            outChannels = 4;
            break;
        case cmsSigLabData:
            outFormat = TYPE_Lab_8;
            outChannels = 3;
            break;
        default:
            outFormat = TYPE_RGB_8;
            outChannels = 3;
            break;
    }

    cmsHTRANSFORM transform = cmsCreateTransform(hIn, inFormat, hOut, outFormat, INTENT_PERCEPTUAL, 0);
    if (!transform) {
        cmsCloseProfile(hIn);
        cmsCloseProfile(hOut);
        return 0;
    }

    // Pixel data is the last pixel_bytes bytes of the original input
    const uint8_t *pixel_data = data + size - pixel_bytes;
    size_t pixel_count = pixel_bytes / inChannels;
    if (pixel_count == 0) pixel_count = 1;

    // Allocate input and output buffers
    size_t in_size = pixel_count * inChannels;
    size_t out_size = pixel_count * outChannels;
    uint8_t *in_buf = (uint8_t *)malloc(in_size);
    uint8_t *out_buf = (uint8_t *)malloc(out_size);
    if (!in_buf || !out_buf) {
        free(in_buf);
        free(out_buf);
        cmsDeleteTransform(transform);
        cmsCloseProfile(hIn);
        cmsCloseProfile(hOut);
        return 0;
    }

    // Copy pixel data, padding if necessary
    size_t copy_size = pixel_bytes < in_size ? pixel_bytes : in_size;
    memcpy(in_buf, pixel_data, copy_size);
    if (copy_size < in_size) {
        memset(in_buf + copy_size, 0, in_size - copy_size);
    }

    cmsDoTransform(transform, in_buf, out_buf, pixel_count);

    free(in_buf);
    free(out_buf);
    cmsDeleteTransform(transform);
    cmsCloseProfile(hIn);
    cmsCloseProfile(hOut);

    return 0;
}