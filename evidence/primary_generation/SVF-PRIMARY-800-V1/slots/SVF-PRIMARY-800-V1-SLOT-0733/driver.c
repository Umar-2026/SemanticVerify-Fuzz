#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <lcms2.h>

int LLVMFuzzerTestOneInput(const unsigned char *data, size_t size) {
    if (size < 8) return 0;

    // Parse input: first 4 bytes for input format, next 4 for output format
    cmsUInt32Number inputFormat = 0;
    cmsUInt32Number outputFormat = 0;
    memcpy(&inputFormat, data, 4);
    memcpy(&outputFormat, data + 4, 4);
    data += 8;
    size -= 8;

    // Limit pixel data size to something reasonable
    if (size > 1024 * 1024) size = 1024 * 1024;

    // Create a simple sRGB to Lab transform (or use generic formats)
    cmsHPROFILE hIn = cmsCreate_sRGBProfile();
    cmsHPROFILE hOut = cmsCreateLab4Profile(NULL);
    if (!hIn || !hOut) {
        if (hIn) cmsCloseProfile(hIn);
        if (hOut) cmsCloseProfile(hOut);
        return 0;
    }

    cmsHTRANSFORM hTransform = cmsCreateTransform(hIn, inputFormat, hOut, outputFormat, INTENT_PERCEPTUAL, 0);
    cmsCloseProfile(hIn);
    cmsCloseProfile(hOut);
    if (!hTransform) return 0;

    // Determine number of pixels based on input format
    cmsUInt32Number inputChannels = T_CHANNELS(inputFormat);
    cmsUInt32Number outputChannels = T_CHANNELS(outputFormat);
    if (inputChannels == 0 || outputChannels == 0) {
        cmsDeleteTransform(hTransform);
        return 0;
    }

    // Bytes per pixel for input and output (assuming 8-bit or 16-bit based on format)
    cmsUInt32Number inputBytesPerPixel = (T_BYTES(inputFormat) ? T_BYTES(inputFormat) : 1) * inputChannels;
    cmsUInt32Number outputBytesPerPixel = (T_BYTES(outputFormat) ? T_BYTES(outputFormat) : 1) * outputChannels;
    if (inputBytesPerPixel == 0 || outputBytesPerPixel == 0) {
        cmsDeleteTransform(hTransform);
        return 0;
    }

    cmsUInt32Number numPixels = size / inputBytesPerPixel;
    if (numPixels == 0) {
        cmsDeleteTransform(hTransform);
        return 0;
    }

    // Allocate output buffer
    size_t outSize = (size_t)numPixels * outputBytesPerPixel;
    unsigned char *outBuf = (unsigned char *)malloc(outSize);
    if (!outBuf) {
        cmsDeleteTransform(hTransform);
        return 0;
    }

    // Process all pixels in one call
    cmsDoTransform(hTransform, (void *)data, outBuf, numPixels);

    // Free resources
    free(outBuf);
    cmsDeleteTransform(hTransform);
    return 0;
}