#include "lcms2.h"
#include <stdint.h>
#include <stdlib.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 128) {
        return 0;
    }

    cmsHPROFILE hProfile1 = cmsOpenProfileFromMem(data, size);
    cmsHPROFILE hProfile2 = cmsCreate_sRGBProfile();

    if (hProfile1 && hProfile2) {
        cmsUInt32Number version1 = cmsGetProfileVersion(hProfile1);
        cmsUInt32Number version2 = cmsGetProfileVersion(hProfile2);

        cmsColorSpaceSignature cs1 = cmsGetColorSpace(hProfile1);
        cmsColorSpaceSignature cs2 = cmsGetColorSpace(hProfile2);

        cmsUInt32Number intent1 = cmsGetHeaderRenderingIntent(hProfile1);
        cmsUInt32Number intent2 = cmsGetHeaderRenderingIntent(hProfile2);

        (void)version1;
        (void)version2;
        (void)cs1;
        (void)cs2;
        (void)intent1;
        (void)intent2;
    }

    if (hProfile1) {
        cmsCloseProfile(hProfile1);
    }
    if (hProfile2) {
        cmsCloseProfile(hProfile2);
    }

    return 0;
}