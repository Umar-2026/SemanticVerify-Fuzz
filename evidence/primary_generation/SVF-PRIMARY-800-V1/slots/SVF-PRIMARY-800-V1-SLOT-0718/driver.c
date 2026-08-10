#include "lcms2.h"
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 16) {
        return 0;
    }

    cmsUInt32Number inputFormat = (cmsUInt32Number)data[0] << 24 | (cmsUInt32Number)data[1] << 16 | (cmsUInt32Number)data[2] << 8 | (cmsUInt32Number)data[3];
    cmsUInt32Number outputFormat = (cmsUInt32Number)data[4] << 24 | (cmsUInt32Number)data[5] << 16 | (cmsUInt32Number)data[6] << 8 | (cmsUInt32Number)data[7];
    cmsUInt32Number intent = (cmsUInt32Number)data[8];
    
    size_t pixelDataSize = size - 16;
    if (pixelDataSize == 0) return 0;

    cmsHPROFILE hInput = cmsCreate_sRGBProfile();
    cmsHPROFILE hOutput = cmsCreate_sRGBProfile();

    if (!hInput || !hOutput) {
        if (hInput) cmsCloseProfile(hInput);
        if (hOutput) cmsCloseProfile(hOutput);
        return 0;
    }

    cmsHTRANSFORM hTransform = cmsCreateTransform(hInput, inputFormat, hOutput, outputFormat, intent, 0);

    if (hTransform) {
        void *outputBuffer = malloc(pixelDataSize);
        if (outputBuffer) {
            cmsDoTransform(hTransform, (const void *)(data + 16), outputBuffer, (cmsUInt32Number)(pixelDataSize / 4));
            free(outputBuffer);
        }
        cmsDeleteTransform(hTransform);
    }

    cmsCloseProfile(hInput);
    cmsCloseProfile(hOutput);

    return 0;
}