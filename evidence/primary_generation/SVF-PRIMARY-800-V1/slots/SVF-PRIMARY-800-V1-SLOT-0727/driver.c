#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include "lcms2.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 4) return 0;

    cmsHPROFILE hProfile = cmsOpenProfileFromMem(data, size);
    if (!hProfile) return 0;

    // Inspect basic profile info
    cmsColorSpaceSignature colorSpace = cmsGetColorSpace(hProfile);
    cmsColorSpaceSignature pcs = cmsGetPCS(hProfile);
    cmsUInt32Number intentCount = cmsGetSupportedIntents(0, NULL);
    (void)colorSpace;
    (void)pcs;
    (void)intentCount;

    // Try to create a transform if profile is output or input capable
    cmsUInt32Number inputFormat = TYPE_RGB_8;
    cmsUInt32Number outputFormat = TYPE_RGB_8;
    cmsHTRANSFORM hTransform = NULL;

    // Attempt transform from profile to Lab if possible
    if (cmsIsMatrixShaper(hProfile)) {
        hTransform = cmsCreateTransform(hProfile, inputFormat, NULL, TYPE_Lab_DBL, INTENT_PERCEPTUAL, 0);
    } else {
        // Try as input profile to Lab
        hTransform = cmsCreateTransform(hProfile, inputFormat, NULL, TYPE_Lab_DBL, INTENT_PERCEPTUAL, 0);
    }

    if (hTransform) {
        // Process a small buffer of pixels
        uint8_t pixels[3 * 16];
        memset(pixels, 0x80, sizeof(pixels));
        double lab[3 * 16];
        cmsDoTransform(hTransform, pixels, lab, 16);
        cmsDeleteTransform(hTransform);
    }

    // Try to create a proofing transform if profile is a device link or output
    cmsHTRANSFORM hProof = cmsCreateProofingTransform(hProfile, inputFormat, NULL, TYPE_Lab_DBL, hProfile, INTENT_PERCEPTUAL, INTENT_ABSOLUTE_COLORIMETRIC, 0);
    if (hProof) {
        uint8_t pixels[3 * 8];
        memset(pixels, 0x40, sizeof(pixels));
        double lab[3 * 8];
        cmsDoTransform(hProof, pixels, lab, 8);
        cmsDeleteTransform(hProof);
    }

    // Attempt to save a copy of the profile to memory
    cmsUInt32Number profileSize = 0;
    cmsSaveProfileToMem(hProfile, NULL, &profileSize);
    if (profileSize > 0 && profileSize <= size * 2 + 1024) {
        uint8_t *buffer = (uint8_t *)malloc(profileSize);
        if (buffer) {
            cmsUInt32Number written = 0;
            if (cmsSaveProfileToMem(hProfile, buffer, &written)) {
                // Verify round-trip
                cmsHPROFILE hCopy = cmsOpenProfileFromMem(buffer, written);
                if (hCopy) {
                    cmsCloseProfile(hCopy);
                }
            }
            free(buffer);
        }
    }

    cmsCloseProfile(hProfile);
    return 0;
}