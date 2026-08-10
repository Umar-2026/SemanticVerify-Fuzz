#include "lcms2.h"
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1) {
        return 0;
    }

    cmsHPROFILE hProfile = cmsOpenProfileFromMem(data, size);
    if (hProfile == NULL) {
        return 0;
    }

    // Inspect basic profile information
    char manufacturer[256];
    char model[256];
    char copyright[256];
    char description[256];

    cmsGetProfileInfoASCII(hProfile, cmsInfoManufacturer, "en", "US", manufacturer, sizeof(manufacturer));
    cmsGetProfileInfoASCII(hProfile, cmsInfoModel, "en", "US", model, sizeof(model));
    cmsGetProfileInfoASCII(hProfile, cmsInfoCopyright, "en", "US", copyright, sizeof(copyright));
    cmsGetProfileInfoASCII(hProfile, cmsInfoDescription, "en", "US", description, sizeof(description));

    // Get color space and PCS
    cmsColorSpaceSignature colorSpace = cmsGetColorSpace(hProfile);
    cmsColorSpaceSignature pcs = cmsGetPCS(hProfile);
    cmsUInt32Number version = cmsGetProfileVersion(hProfile);
    cmsUInt32Number deviceClass = cmsGetDeviceClass(hProfile);
    cmsUInt32Number renderingIntent = cmsGetHeaderRenderingIntent(hProfile);

    // Get profile ID if present
    cmsUInt8Number profileID[16];
    cmsGetHeaderProfileID(hProfile, profileID);

    // Check for tags
    cmsBool hasA2B0 = cmsIsTag(hProfile, cmsSigAToB0Tag);
    cmsBool hasB2A0 = cmsIsTag(hProfile, cmsSigBToA0Tag);
    cmsBool hasGamut = cmsIsTag(hProfile, cmsSigGamutTag);

    // Get tag count
    cmsInt32Number tagCount = cmsGetTagCount(hProfile);

    // Iterate over tags and get signatures
    for (cmsInt32Number i = 0; i < tagCount; i++) {
        cmsTagSignature sig = cmsGetTagSignature(hProfile, i);
        // Just access the signature to ensure it's valid
        (void)sig;
    }

    // Close the profile
    cmsCloseProfile(hProfile);

    return 0;
}