#include "lcms2.h"
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 4) return 0;

    cmsHPROFILE hProfile = cmsOpenProfileFromMem(data, size);
    if (!hProfile) return 0;

    // Basic inspection: get profile info
    char info[256];
    cmsGetProfileInfoASCII(hProfile, cmsInfoDescription, "en", "US", info, sizeof(info));

    // Try to create a transform from the profile to sRGB if possible
    cmsHPROFILE hSRGB = cmsCreate_sRGBProfile();
    if (hSRGB) {
        cmsHTRANSFORM hTransform = cmsCreateTransform(hProfile, TYPE_RGB_8, hSRGB, TYPE_RGB_8, INTENT_PERCEPTUAL, 0);
        if (hTransform) {
            // Process a small amount of data if the input is large enough
            if (size >= 16) {
                uint8_t in[3] = {data[0], data[1], data[2]};
                uint8_t out[3] = {0, 0, 0};
                cmsDoTransform(hTransform, in, out, 1);
            }
            cmsDeleteTransform(hTransform);
        }
        cmsCloseProfile(hSRGB);
    }

    // Try to create a transform from sRGB to the profile
    hSRGB = cmsCreate_sRGBProfile();
    if (hSRGB) {
        cmsHTRANSFORM hTransform = cmsCreateTransform(hSRGB, TYPE_RGB_8, hProfile, TYPE_RGB_8, INTENT_PERCEPTUAL, 0);
        if (hTransform) {
            if (size >= 16) {
                uint8_t in[3] = {data[4], data[5], data[6]};
                uint8_t out[3] = {0, 0, 0};
                cmsDoTransform(hTransform, in, out, 1);
            }
            cmsDeleteTransform(hTransform);
        }
        cmsCloseProfile(hSRGB);
    }

    // Try to save the profile to memory (round-trip)
    cmsUInt32Number bytesNeeded = 0;
    if (cmsSaveProfileToMem(hProfile, NULL, &bytesNeeded) && bytesNeeded > 0) {
        uint8_t *buf = (uint8_t *)malloc(bytesNeeded);
        if (buf) {
            cmsUInt32Number bytesWritten = 0;
            cmsSaveProfileToMem(hProfile, buf, &bytesWritten);
            free(buf);
        }
    }

    cmsCloseProfile(hProfile);
    return 0;
}