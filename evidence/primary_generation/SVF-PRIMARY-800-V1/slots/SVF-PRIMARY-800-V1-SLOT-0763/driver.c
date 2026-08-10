#include "lcms2.h"
#include <stdint.h>
#include <string.h>
#include <stdlib.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

    // Split input into two halves for two profiles
    size_t half = size / 2;
    const uint8_t *data1 = data;
    size_t size1 = half;
    const uint8_t *data2 = data + half;
    size_t size2 = size - half;

    cmsHPROFILE h1 = NULL;
    cmsHPROFILE h2 = NULL;

    // First profile: try to open from memory, if that fails create sRGB
    h1 = cmsOpenProfileFromMem(data1, size1);
    if (!h1) {
        h1 = cmsCreate_sRGBProfile();
    }

    // Second profile: try to open from memory, if that fails create sRGB
    h2 = cmsOpenProfileFromMem(data2, size2);
    if (!h2) {
        h2 = cmsCreate_sRGBProfile();
    }

    if (!h1 || !h2) {
        if (h1) cmsCloseProfile(h1);
        if (h2) cmsCloseProfile(h2);
        return 0;
    }

    // Inspect information from each profile
    cmsInfoType infoTypes[] = {
        cmsInfoDescription,
        cmsInfoManufacturer,
        cmsInfoModel,
        cmsInfoCopyright
    };

    for (int i = 0; i < 4; i++) {
        // Query profile 1
        cmsUInt32Number len1 = cmsGetProfileInfo(h1, infoTypes[i], "en", "US", NULL, 0);
        if (len1 > 0 && len1 < 1024) {
            char *buf1 = (char *)malloc(len1);
            if (buf1) {
                cmsGetProfileInfo(h1, infoTypes[i], "en", "US", buf1, len1);
                free(buf1);
            }
        }

        // Query profile 2
        cmsUInt32Number len2 = cmsGetProfileInfo(h2, infoTypes[i], "en", "US", NULL, 0);
        if (len2 > 0 && len2 < 1024) {
            char *buf2 = (char *)malloc(len2);
            if (buf2) {
                cmsGetProfileInfo(h2, infoTypes[i], "en", "US", buf2, len2);
                free(buf2);
            }
        }
    }

    // Get color space and PCS for both profiles
    cmsColorSpaceSignature cs1 = cmsGetColorSpace(h1);
    cmsColorSpaceSignature cs2 = cmsGetColorSpace(h2);
    cmsColorSpaceSignature pcs1 = cmsGetPCS(h1);
    cmsColorSpaceSignature pcs2 = cmsGetPCS(h2);

    // Get device class
    cmsProfileClassSignature class1 = cmsGetDeviceClass(h1);
    cmsProfileClassSignature class2 = cmsGetDeviceClass(h2);

    // Get rendering intent
    cmsUInt32Number intent1 = cmsGetHeaderRenderingIntent(h1);
    cmsUInt32Number intent2 = cmsGetHeaderRenderingIntent(h2);

    // Get version
    cmsFloat64Number version1 = cmsGetProfileVersion(h1);
    cmsFloat64Number version2 = cmsGetProfileVersion(h2);

    // Get flags
    cmsUInt32Number flags1 = cmsGetHeaderFlags(h1);
    cmsUInt32Number flags2 = cmsGetHeaderFlags(h2);

    // Get manufacturer and model from header
    cmsUInt32Number manufacturer1 = cmsGetHeaderManufacturer(h1);
    cmsUInt32Number manufacturer2 = cmsGetHeaderManufacturer(h2);
    cmsUInt32Number model1 = cmsGetHeaderModel(h1);
    cmsUInt32Number model2 = cmsGetHeaderModel(h2);

    // Get attributes
    cmsUInt64Number attributes1 = cmsGetHeaderAttributes(h1);
    cmsUInt64Number attributes2 = cmsGetHeaderAttributes(h2);

    // Get creator
    cmsUInt32Number creator1 = cmsGetHeaderCreator(h1);
    cmsUInt32Number creator2 = cmsGetHeaderCreator(h2);

    // Get profile ID
    cmsUInt8Number profileID1[16];
    cmsUInt8Number profileID2[16];
    cmsGetHeaderProfileID(h1, profileID1);
    cmsGetHeaderProfileID(h2, profileID2);

    // Get tag count and iterate tags
    cmsInt32Number tagCount1 = cmsGetTagCount(h1);
    cmsInt32Number tagCount2 = cmsGetTagCount(h2);

    for (cmsInt32Number i = 0; i < tagCount1 && i < 100; i++) {
        cmsTagSignature sig = cmsGetTagSignature(h1, i);
        if (cmsIsTag(h1, sig)) {
            cmsUInt32Number tagSize = cmsReadRawTag(h1, sig, NULL, 0);
            if (tagSize > 0 && tagSize < 4096) {
                void *tagData = malloc(tagSize);
                if (tagData) {
                    cmsReadRawTag(h1, sig, tagData, tagSize);
                    free(tagData);
                }
            }
        }
    }

    for (cmsInt32Number i = 0; i < tagCount2 && i < 100; i++) {
        cmsTagSignature sig = cmsGetTagSignature(h2, i);
        if (cmsIsTag(h2, sig)) {
            cmsUInt32Number tagSize = cmsReadRawTag(h2, sig, NULL, 0);
            if (tagSize > 0 && tagSize < 4096) {
                void *tagData = malloc(tagSize);
                if (tagData) {
                    cmsReadRawTag(h2, sig, tagData, tagSize);
                    free(tagData);
                }
            }
        }
    }

    // Check if profiles are matrix-shaper or cLUT based
    cmsBool isMatrix1 = cmsIsMatrixShaper(h1);
    cmsBool isMatrix2 = cmsIsMatrixShaper(h2);
    cmsBool isCLUT1 = cmsIsCLUT(h1, 0, 1);
    cmsBool isCLUT2 = cmsIsCLUT(h2, 0, 1);

    // Get intent for proofing
    cmsUInt32Number proofIntent1 = cmsGetHeaderRenderingIntent(h1);
    cmsUInt32Number proofIntent2 = cmsGetHeaderRenderingIntent(h2);

    // Use variables to prevent optimization
    volatile cmsUInt32Number dummy = 0;
    dummy += cs1 + cs2 + pcs1 + pcs2 + class1 + class2 + intent1 + intent2;
    dummy += (cmsUInt32Number)version1 + (cmsUInt32Number)version2 + flags1 + flags2;
    dummy += manufacturer1 + manufacturer2 + model1 + model2;
    dummy += (cmsUInt32Number)(attributes1 & 0xFFFFFFFF) + (cmsUInt32Number)(attributes2 & 0xFFFFFFFF);
    dummy += creator1 + creator2;
    dummy += profileID1[0] + profileID2[0];
    dummy += (cmsUInt32Number)tagCount1 + (cmsUInt32Number)tagCount2;
    dummy += (cmsUInt32Number)isMatrix1 + (cmsUInt32Number)isMatrix2 + (cmsUInt32Number)isCLUT1 + (cmsUInt32Number)isCLUT2;
    dummy += proofIntent1 + proofIntent2;

    (void)dummy;

    cmsCloseProfile(h1);
    cmsCloseProfile(h2);

    return 0;
}