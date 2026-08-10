#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include "lcms2.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

    cmsHPROFILE hProfile = cmsOpenProfileFromMem(data, size);
    if (hProfile == NULL) return 0;

    // Inspect profile basic info
    cmsUInt32Number version = cmsGetProfileVersion(hProfile);
    (void)version;

    cmsUInt32Number deviceClass = cmsGetDeviceClass(hProfile);
    (void)deviceClass;

    cmsUInt32Number colorSpace = cmsGetColorSpace(hProfile);
    (void)colorSpace;

    cmsUInt32Number pcs = cmsGetPCS(hProfile);
    (void)pcs;

    // Try to create a transform if profile has input and output spaces
    if (colorSpace != 0 && pcs != 0) {
        cmsHPROFILE hPCS = cmsCreateLab4Profile(NULL);
        if (hPCS != NULL) {
            cmsHTRANSFORM hTransform = cmsCreateTransform(hProfile, colorSpace, hPCS, TYPE_Lab_DBL, INTENT_PERCEPTUAL, 0);
            if (hTransform != NULL) {
                // Transform a small set of sample values
                double input[3] = {0.5, 0.5, 0.5};
                double output[3] = {0.0, 0.0, 0.0};
                cmsDoTransform(hTransform, input, output, 1);
                cmsDeleteTransform(hTransform);
            }
            cmsCloseProfile(hPCS);
        }
    }

    // Try to save the profile to memory (round-trip)
    cmsUInt32Number bytesNeeded = 0;
    if (cmsSaveProfileToMem(hProfile, NULL, &bytesNeeded) && bytesNeeded > 0) {
        uint8_t *buffer = (uint8_t *)malloc(bytesNeeded);
        if (buffer != NULL) {
            cmsUInt32Number bytesWritten = 0;
            if (cmsSaveProfileToMem(hProfile, buffer, &bytesWritten)) {
                // Optionally re-open the saved profile to verify integrity
                cmsHPROFILE hReopened = cmsOpenProfileFromMem(buffer, bytesWritten);
                if (hReopened != NULL) {
                    cmsCloseProfile(hReopened);
                }
            }
            free(buffer);
        }
    }

    cmsCloseProfile(hProfile);
    return 0;
}