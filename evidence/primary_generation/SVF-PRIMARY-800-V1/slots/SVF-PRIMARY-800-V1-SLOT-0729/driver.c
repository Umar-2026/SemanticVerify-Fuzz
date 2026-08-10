#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include "lcms2.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 4) return 0;

    cmsHPROFILE hProfile = cmsOpenProfileFromMem(data, size);
    if (hProfile == NULL) return 0;

    // Inspect profile basic info
    cmsColorSpaceSignature colorSpace = cmsGetColorSpace(hProfile);
    cmsColorSpaceSignature pcs = cmsGetPCS(hProfile);
    cmsUInt32Number intentCount = cmsGetSupportedIntents(0, NULL);
    (void)colorSpace;
    (void)pcs;
    (void)intentCount;

    // Try to create a transform if profile is output or input capable
    cmsHPROFILE hLab = cmsCreateLab4Profile(NULL);
    if (hLab != NULL) {
        cmsHTRANSFORM hTransform = NULL;
        // Attempt transform from profile to Lab
        if (cmsIsMatrixShaper(hProfile) || cmsGetDeviceClass(hProfile) == cmsSigInputClass) {
            hTransform = cmsCreateTransform(hProfile, TYPE_RGB_8, hLab, TYPE_Lab_DBL, INTENT_PERCEPTUAL, 0);
        } else if (cmsGetDeviceClass(hProfile) == cmsSigOutputClass) {
            hTransform = cmsCreateTransform(hLab, TYPE_Lab_DBL, hProfile, TYPE_RGB_8, INTENT_PERCEPTUAL, 0);
        }
        if (hTransform != NULL) {
            // Apply transform to a small set of pixels derived from input data
            cmsUInt8Number rgb[3] = { (cmsUInt8Number)(data[0] & 0xFF), (cmsUInt8Number)(data[1] & 0xFF), (cmsUInt8Number)(data[2] & 0xFF) };
            cmsCIELab lab;
            if (cmsGetDeviceClass(hProfile) == cmsSigInputClass) {
                cmsDoTransform(hTransform, rgb, &lab, 1);
            } else if (cmsGetDeviceClass(hProfile) == cmsSigOutputClass) {
                cmsCIELab labIn = { 50.0, 0.0, 0.0 };
                cmsDoTransform(hTransform, &labIn, rgb, 1);
            }
            cmsDeleteTransform(hTransform);
        }
        cmsCloseProfile(hLab);
    }

    // Try to save profile to memory (round-trip)
    cmsUInt32Number bytesNeeded = 0;
    if (cmsSaveProfileToMem(hProfile, NULL, &bytesNeeded) && bytesNeeded > 0) {
        cmsUInt8Number *buffer = (cmsUInt8Number *)malloc(bytesNeeded);
        if (buffer != NULL) {
            cmsUInt32Number bytesWritten = 0;
            if (cmsSaveProfileToMem(hProfile, buffer, &bytesWritten)) {
                // Successfully wrote profile; no further action needed
            }
            free(buffer);
        }
    }

    cmsCloseProfile(hProfile);
    return 0;
}