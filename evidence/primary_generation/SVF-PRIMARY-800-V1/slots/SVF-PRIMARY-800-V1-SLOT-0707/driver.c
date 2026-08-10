#include "lcms2.h"
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size == 0) {
        return 0;
    }

    cmsHPROFILE hProfile = cmsOpenProfileFromMem(data, size);
    if (hProfile == NULL) {
        return 0;
    }

    // Inspect basic profile information
    cmsInfoType infoTypes[] = {
        cmsInfoDescription,
        cmsInfoManufacturer,
        cmsInfoModel,
        cmsInfoCopyright
    };

    char buffer[256];
    for (size_t i = 0; i < sizeof(infoTypes) / sizeof(infoTypes[0]); i++) {
        cmsGetProfileInfoASCII(hProfile, infoTypes[i], "en", "US", buffer, sizeof(buffer));
    }

    // Get color space and profile class
    cmsColorSpaceSignature colorSpace = cmsGetColorSpace(hProfile);
    cmsColorSpaceSignature pcs = cmsGetPCS(hProfile);
    cmsProfileClassSignature profileClass = cmsGetDeviceClass(hProfile);

    // Get version and rendering intent
    cmsFloat64Number version = cmsGetProfileVersion(hProfile);
    cmsUInt32Number intent = cmsGetHeaderRenderingIntent(hProfile);

    // Get number of tags
    cmsInt32Number tagCount = cmsGetTagCount(hProfile);
    if (tagCount > 0) {
        cmsTagSignature sig = cmsGetTagSignature(hProfile, 0);
        (void)sig;
    }

    // Attempt to create a transform from this profile to sRGB
    cmsHPROFILE hSRGB = cmsCreate_sRGBProfile();
    if (hSRGB != NULL) {
        cmsHTRANSFORM hTransform = cmsCreateTransform(hProfile, TYPE_RGB_8, hSRGB, TYPE_RGB_8, INTENT_PERCEPTUAL, 0);
        if (hTransform != NULL) {
            // Process a small buffer to exercise the transform
            uint8_t input[3] = {128, 128, 128};
            uint8_t output[3] = {0, 0, 0};
            cmsDoTransform(hTransform, input, output, 1);
            cmsDeleteTransform(hTransform);
        }
        cmsCloseProfile(hSRGB);
    }

    // Close the profile
    cmsCloseProfile(hProfile);

    return 0;
}