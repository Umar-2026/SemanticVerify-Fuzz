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
    const char *languageCode = "en";
    const char *countryCode = "US";

    for (int i = 0; i < 4; i++) {
        // Profile 1 info
        cmsUInt32Number len1 = cmsGetProfileInfo(hProfile1, infoTypes[i], languageCode, countryCode, NULL, 0);
        if (len1 > 0 && len1 < 1024) {
            char *buf1 = (char *)malloc(len1);
            if (buf1) {
                cmsGetProfileInfo(hProfile1, infoTypes[i], languageCode, countryCode, buf1, len1);
                free(buf1);
            }
        }

        // Profile 2 info
        cmsUInt32Number len2 = cmsGetProfileInfo(hProfile2, infoTypes[i], languageCode, countryCode, NULL, 0);
        if (len2 > 0 && len2 < 1024) {
            char *buf2 = (char *)malloc(len2);
            if (buf2) {
                cmsGetProfileInfo(hProfile2, infoTypes[i], languageCode, countryCode, buf2, len2);
                free(buf2);
            }
        }
    }

    // Additional inspection: color space and PCS
    cmsColorSpaceSignature cs1 = cmsGetColorSpace(hProfile1);
    cmsColorSpaceSignature cs2 = cmsGetColorSpace(hProfile2);
    cmsColorSpaceSignature pcs1 = cmsGetPCS(hProfile1);
    cmsColorSpaceSignature pcs2 = cmsGetPCS(hProfile2);

    // Use the values to prevent optimization
    volatile cmsColorSpaceSignature v_cs1 = cs1;
    volatile cmsColorSpaceSignature v_cs2 = cs2;
    volatile cmsColorSpaceSignature v_pcs1 = pcs1;
    volatile cmsColorSpaceSignature v_pcs2 = pcs2;
    (void)v_cs1; (void)v_cs2; (void)v_pcs1; (void)v_pcs2;

    // Cleanup
    cmsCloseProfile(hProfile1);
    cmsCloseProfile(hProfile2);

    return 0;
}