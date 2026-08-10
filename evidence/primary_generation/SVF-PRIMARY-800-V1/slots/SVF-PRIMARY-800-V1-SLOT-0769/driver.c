#include "lcms2.h"
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

    // Split input into two halves for two profiles
    size_t half = size / 2;
    const uint8_t *data1 = data;
    size_t size1 = half;
    const uint8_t *data2 = data + half;
    size_t size2 = size - half;

    cmsHPROFILE hProfile1 = NULL;
    cmsHPROFILE hProfile2 = NULL;

    // First profile: try to open from memory, fallback to sRGB
    if (size1 > 0) {
        hProfile1 = cmsOpenProfileFromMem(data1, size1);
    }
    if (!hProfile1) {
        hProfile1 = cmsCreate_sRGBProfile();
    }

    // Second profile: try to open from memory, fallback to sRGB
    if (size2 > 0) {
        hProfile2 = cmsOpenProfileFromMem(data2, size2);
    }
    if (!hProfile2) {
        hProfile2 = cmsCreate_sRGBProfile();
    }

    if (!hProfile1 || !hProfile2) {
        if (hProfile1) cmsCloseProfile(hProfile1);
        if (hProfile2) cmsCloseProfile(hProfile2);
        return 0;
    }

    // Inspect information from each profile
    cmsInfoType infoTypes[] = {
        cmsInfoDescription,
        cmsInfoManufacturer,
        cmsInfoModel,
        cmsInfoCopyright
    };
    const char *langCode = "en";
    const char *countryCode = "US";

    for (int i = 0; i < 4; i++) {
        // Profile 1 info
        cmsUInt32Number len1 = cmsGetProfileInfo(hProfile1, infoTypes[i], langCode, countryCode, NULL, 0);
        if (len1 > 0 && len1 < 1024) {
            char *buf1 = (char *)malloc(len1);
            if (buf1) {
                cmsGetProfileInfo(hProfile1, infoTypes[i], langCode, countryCode, buf1, len1);
                free(buf1);
            }
        }

        // Profile 2 info
        cmsUInt32Number len2 = cmsGetProfileInfo(hProfile2, infoTypes[i], langCode, countryCode, NULL, 0);
        if (len2 > 0 && len2 < 1024) {
            char *buf2 = (char *)malloc(len2);
            if (buf2) {
                cmsGetProfileInfo(hProfile2, infoTypes[i], langCode, countryCode, buf2, len2);
                free(buf2);
            }
        }
    }

    // Additional inspection: color space, version, device class
    cmsColorSpaceSignature cs1 = cmsGetColorSpace(hProfile1);
    cmsColorSpaceSignature cs2 = cmsGetColorSpace(hProfile2);
    cmsUInt32Number version1 = cmsGetProfileVersion(hProfile1);
    cmsUInt32Number version2 = cmsGetProfileVersion(hProfile2);
    cmsProfileClassSignature class1 = cmsGetDeviceClass(hProfile1);
    cmsProfileClassSignature class2 = cmsGetDeviceClass(hProfile2);

    // Use the values to prevent optimization
    volatile cmsColorSpaceSignature vcs1 = cs1;
    volatile cmsColorSpaceSignature vcs2 = cs2;
    volatile cmsUInt32Number vv1 = version1;
    volatile cmsUInt32Number vv2 = version2;
    volatile cmsProfileClassSignature vclass1 = class1;
    volatile cmsProfileClassSignature vclass2 = class2;
    (void)vcs1; (void)vcs2; (void)vv1; (void)vv2; (void)vclass1; (void)vclass2;

    // Cleanup
    cmsCloseProfile(hProfile1);
    cmsCloseProfile(hProfile2);

    return 0;
}