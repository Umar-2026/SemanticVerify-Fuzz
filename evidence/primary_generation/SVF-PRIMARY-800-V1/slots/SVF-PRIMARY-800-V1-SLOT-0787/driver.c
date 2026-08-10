#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include "lcms2.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

    cmsHPROFILE hProfile = cmsOpenProfileFromMem(data, size);
    if (hProfile) {
        cmsHTRANSFORM hTransform = cmsCreateTransform(hProfile, TYPE_RGB_8, hProfile, TYPE_RGB_8, INTENT_PERCEPTUAL, 0);
        if (hTransform) {
            uint8_t *buf = (uint8_t *)malloc(size);
            if (buf) {
                memcpy(buf, data, size);
                cmsDoTransform(hTransform, buf, buf, size / 3);
                free(buf);
            }
            cmsDeleteTransform(hTransform);
        }
        cmsCloseProfile(hProfile);
    } else {
        // If profile open fails, try creating a transform with NULL profile (should fail)
        cmsHTRANSFORM hTransform = cmsCreateTransform(NULL, TYPE_RGB_8, NULL, TYPE_RGB_8, INTENT_PERCEPTUAL, 0);
        if (hTransform) {
            cmsDeleteTransform(hTransform);
        }
    }
    return 0;
}