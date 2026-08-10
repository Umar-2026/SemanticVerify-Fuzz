#include "lcms2.h"
#include <stdint.h>
#include <stddef.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1) {
        return 0;
    }

    cmsHPROFILE hProfile = cmsOpenProfileFromMem(data, size);
    if (hProfile != NULL) {
        cmsUInt32Number profileVersion = cmsGetProfileVersion(hProfile);
        cmsColorSpaceSignature colorSpace = cmsGetColorSpace(hProfile);
        cmsColorSpaceSignature pcs = cmsGetPCS(hProfile);
        
        cmsUInt32Number tagCount = cmsGetTagCount(hProfile);
        if (tagCount > 0) {
            cmsTagSignature tagSig = cmsGetTagSignature(hProfile, 0);
            cmsTagTypeSignature tagType = cmsGetTagType(hProfile, tagSig);
            
            void* tagData = cmsReadTag(hProfile, tagSig);
            if (tagData != NULL) {
                cmsMLU* mlu = cmsMLUalloc(NULL, 1);
                if (mlu) {
                    cmsMLUfree(mlu);
                }
            }
        }

        cmsHTRANSFORM hTransform = cmsCreateTransform(hProfile, TYPE_RGB_8, hProfile, TYPE_RGB_8, INTENT_PERCEPTUAL, 0);
        if (hTransform != NULL) {
            uint8_t input[3] = {128, 128, 128};
            uint8_t output[3];
            cmsDoTransform(hTransform, input, output, 1);
            cmsDeleteTransform(hTransform);
        }

        cmsCloseProfile(hProfile);
    }

    return 0;
}