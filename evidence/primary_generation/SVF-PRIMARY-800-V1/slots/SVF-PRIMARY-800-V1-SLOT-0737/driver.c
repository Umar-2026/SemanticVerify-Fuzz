#include "lcms2.h"
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 16) return 0;

    // Extract parameters from fuzz input
    cmsUInt32Number inputFormat = data[0] | (data[1] << 8) | (data[2] << 16) | ((cmsUInt32Number)data[3] << 24);
    cmsUInt32Number outputFormat = data[4] | (data[5] << 8) | (data[6] << 16) | ((cmsUInt32Number)data[7] << 24);
    cmsUInt32Number nPixels = data[8] | (data[9] << 8) | (data[10] << 16) | ((cmsUInt32Number)data[11] << 24);
    cmsUInt32Number intent = data[12] | (data[13] << 8) | (data[14] << 16) | ((cmsUInt32Number)data[15] << 24);

    // Limit nPixels to avoid excessive memory usage
    if (nPixels > 1024) nPixels = 1024;

    // Determine input and output sizes based on formats (simplified: assume 4 bytes per pixel for common formats)
    // We'll just use a fixed stride of 4 bytes per pixel for both input and output.
    size_t inputBytes = (size_t)nPixels * 4;
    size_t outputBytes = (size_t)nPixels * 4;

    // Ensure we have enough input data for the pixel block
    if (size < 16 + inputBytes) return 0;

    const uint8_t *pixelData = data + 16;

    // Create a simple sRGB profile for input and output (use built-in)
    cmsHPROFILE hIn = cmsCreate_sRGBProfile();
    cmsHPROFILE hOut = cmsCreate_sRGBProfile();
    if (!hIn || !hOut) {
        if (hIn) cmsCloseProfile(hIn);
        if (hOut) cmsCloseProfile(hOut);
        return 0;
    }

    // Create transform
    cmsHTRANSFORM hTransform = cmsCreateTransform(hIn, inputFormat, hOut, outputFormat, intent, 0);
    if (!hTransform) {
        cmsCloseProfile(hIn);
        cmsCloseProfile(hOut);
        return 0;
    }

    // Allocate output buffer
    uint8_t *output = (uint8_t *)malloc(outputBytes);
    if (!output) {
        cmsDeleteTransform(hTransform);
        cmsCloseProfile(hIn);
        cmsCloseProfile(hOut);
        return 0;
    }

    // Process the pixel block
    cmsDoTransform(hTransform, (void *)pixelData, output, nPixels);

    // Cleanup
    free(output);
    cmsDeleteTransform(hTransform);
    cmsCloseProfile(hIn);
    cmsCloseProfile(hOut);

    return 0;
}