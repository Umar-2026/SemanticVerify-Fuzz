#include "lcms2.h"
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 16) return 0;

    // Extract bounded parameters from fuzz input
    uint32_t intent = data[0] % 4;          // 0..3
    uint32_t inFormat = data[1] % 8;        // 0..7
    uint32_t outFormat = data[2] % 8;       // 0..7
    uint32_t flags = data[3] & 0x03;        // 0..3

    // Map format codes to lcms formats (8-bit, 16-bit, float variants)
    uint32_t formats[] = {
        TYPE_GRAY_8,
        TYPE_GRAY_16,
        TYPE_RGB_8,
        TYPE_RGB_16,
        TYPE_RGB_FLT,
        TYPE_CMYK_8,
        TYPE_CMYK_16,
        TYPE_CMYK_FLT
    };
    if (inFormat >= 8 || outFormat >= 8) return 0;
    uint32_t inFmt = formats[inFormat];
    uint32_t outFmt = formats[outFormat];

    // Determine input pixel size based on format
    size_t inPixelSize = 0;
    switch (inFmt) {
        case TYPE_GRAY_8: inPixelSize = 1; break;
        case TYPE_GRAY_16: inPixelSize = 2; break;
        case TYPE_RGB_8: inPixelSize = 3; break;
        case TYPE_RGB_16: inPixelSize = 6; break;
        case TYPE_RGB_FLT: inPixelSize = 12; break;
        case TYPE_CMYK_8: inPixelSize = 4; break;
        case TYPE_CMYK_16: inPixelSize = 8; break;
        case TYPE_CMYK_FLT: inPixelSize = 16; break;
        default: return 0;
    }

    // Determine output pixel size
    size_t outPixelSize = 0;
    switch (outFmt) {
        case TYPE_GRAY_8: outPixelSize = 1; break;
        case TYPE_GRAY_16: outPixelSize = 2; break;
        case TYPE_RGB_8: outPixelSize = 3; break;
        case TYPE_RGB_16: outPixelSize = 6; break;
        case TYPE_RGB_FLT: outPixelSize = 12; break;
        case TYPE_CMYK_8: outPixelSize = 4; break;
        case TYPE_CMYK_16: outPixelSize = 8; break;
        case TYPE_CMYK_FLT: outPixelSize = 16; break;
        default: return 0;
    }

    // Use remaining data as pixel data (at least one pixel)
    size_t avail = size - 4;
    if (avail < inPixelSize) return 0;
    size_t numPixels = avail / inPixelSize;
    if (numPixels == 0) return 0;

    const uint8_t *pixelData = data + 4;
    size_t dataBytes = numPixels * inPixelSize;

    // Create a simple sRGB profile for input and output
    cmsHPROFILE inProfile = cmsCreate_sRGBProfile();
    cmsHPROFILE outProfile = cmsCreate_sRGBProfile();
    if (!inProfile || !outProfile) {
        if (inProfile) cmsCloseProfile(inProfile);
        if (outProfile) cmsCloseProfile(outProfile);
        return 0;
    }

    // Create transform
    cmsHTRANSFORM transform = cmsCreateTransform(inProfile, inFmt, outProfile, outFmt, intent, flags);
    cmsCloseProfile(inProfile);
    cmsCloseProfile(outProfile);
    if (!transform) return 0;

    // Allocate output buffer
    size_t outBytes = numPixels * outPixelSize;
    uint8_t *outBuf = (uint8_t *)malloc(outBytes);
    if (!outBuf) {
        cmsDeleteTransform(transform);
        return 0;
    }

    // Process pixels
    cmsDoTransform(transform, (void *)pixelData, outBuf, (unsigned int)numPixels);

    // Cleanup
    free(outBuf);
    cmsDeleteTransform(transform);

    return 0;
}