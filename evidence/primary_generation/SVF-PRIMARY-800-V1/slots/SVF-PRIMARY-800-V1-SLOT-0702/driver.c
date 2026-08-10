#include <stdint.h>
#include <stddef.h>
#include "lcms2.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1) {
        return 0;
    }

    cmsHPROFILE hProfile = cmsOpenProfileFromMem(data, size);
    if (hProfile != NULL) {
        cmsUInt32Number version = cmsGetProfileVersion(hProfile);
        cmsColorSpaceSignature colorSpace = cmsGetColorSpace(hProfile);
        cmsColorSpaceSignature pcs = cmsGetPCS(hProfile);
        cmsDeviceClass deviceClass = cmsGetDeviceClass(hProfile);

        cmsUInt32Number tagCount = cmsGetTagCount(hProfile);
        if (tagCount > 0) {
            cmsTagSignature tagSig = cmsGetTagSignature(hProfile, 0);
            (void)tagSig;
        }

        cmsCloseProfile(hProfile);
    }

    return 0;
}