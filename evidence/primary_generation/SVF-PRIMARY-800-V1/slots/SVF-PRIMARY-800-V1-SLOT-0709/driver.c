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
    cmsColorSpaceSignature colorSpace = cmsGetColorSpace(hProfile);
    cmsColorSpaceSignature pcs = cmsGetPCS(hProfile);
    cmsUInt32Number deviceClass = cmsGetDeviceClass(hProfile);
    cmsUInt32Number renditionIntent = cmsGetHeaderRenderingIntent(hProfile);
    cmsUInt32Number flags = cmsGetHeaderFlags(hProfile);
    cmsUInt32Number manufacturer = cmsGetHeaderManufacturer(hProfile);
    cmsUInt32Number model = cmsGetHeaderModel(hProfile);
    cmsUInt64Number attributes = cmsGetHeaderAttributes(hProfile);
    cmsUInt32Number version = cmsGetProfileVersion(hProfile);
    cmsUInt32Number profileID[4];
    cmsGetHeaderProfileID(hProfile, profileID);

    // Check if profile is suitable for transforms
    cmsBool isMatrixShaper = cmsIsMatrixShaper(hProfile);
    cmsBool isCLM = cmsIsCLM(hProfile);
    cmsUInt32Number tagCount = cmsGetTagCount(hProfile);

    // Iterate over tags and inspect some common ones
    for (cmsUInt32Number i = 0; i < tagCount && i < 100; i++) {
        cmsTagSignature sig = cmsGetTagSignature(hProfile, i);
        if (sig == cmsSigProfileDescriptionTag) {
            cmsMLU *mlu = (cmsMLU *)cmsReadTag(hProfile, sig);
            if (mlu != NULL) {
                char buffer[256];
                cmsUInt32Number len = cmsMLUgetASCII(mlu, cmsGetLanguageCode(mlu, 0), cmsGetCountryCode(mlu, 0), buffer, sizeof(buffer));
                (void)len;
            }
        } else if (sig == cmsSigCopyrightTag) {
            cmsMLU *mlu = (cmsMLU *)cmsReadTag(hProfile, sig);
            if (mlu != NULL) {
                char buffer[256];
                cmsUInt32Number len = cmsMLUgetASCII(mlu, cmsGetLanguageCode(mlu, 0), cmsGetCountryCode(mlu, 0), buffer, sizeof(buffer));
                (void)len;
            }
        } else if (sig == cmsSigMediaWhitePointTag) {
            cmsCIEXYZ *wp = (cmsCIEXYZ *)cmsReadTag(hProfile, sig);
            if (wp != NULL) {
                (void)wp->X;
                (void)wp->Y;
                (void)wp->Z;
            }
        } else if (sig == cmsSigChromaticAdaptationTag) {
            cmsCIEXYZ *adapt = (cmsCIEXYZ *)cmsReadTag(hProfile, sig);
            if (adapt != NULL) {
                (void)adapt->X;
                (void)adapt->Y;
                (void)adapt->Z;
            }
        }
    }

    // Attempt to create a transform if profile is an input or display profile
    if (deviceClass == cmsSigInputClass || deviceClass == cmsSigDisplayClass) {
        cmsHPROFILE hLab = cmsCreateLab4Profile(NULL);
        if (hLab != NULL) {
            cmsHTRANSFORM hTransform = cmsCreateTransform(hProfile, TYPE_RGB_8, hLab, TYPE_Lab_DBL, INTENT_PERCEPTUAL, 0);
            if (hTransform != NULL) {
                // Process a small amount of data
                unsigned char rgb[3] = {128, 128, 128};
                double lab[3];
                cmsDoTransform(hTransform, rgb, lab, 1);
                cmsDeleteTransform(hTransform);
            }
            cmsCloseProfile(hLab);
        }
    }

    cmsCloseProfile(hProfile);
    return 0;
}