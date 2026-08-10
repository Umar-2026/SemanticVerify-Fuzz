#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "lcms2.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

    cmsHPROFILE hProfile = cmsOpenProfileFromMem(data, size);
    if (hProfile) {
        cmsHPROFILE hLab = cmsCreateLab4Profile(NULL);
        if (hLab) {
            cmsHTRANSFORM hTransform = cmsCreateTransform(hProfile, TYPE_RGB_8, hLab, TYPE_Lab_8, INTENT_PERCEPTUAL, 0);
            if (hTransform) {
                unsigned char in[3] = {0, 0, 0};
                unsigned char out[3] = {0, 0, 0};
                cmsDoTransform(hTransform, in, out, 1);
                cmsDeleteTransform(hTransform);
            } else {
                cmsHTRANSFORM hTransform2 = cmsCreateTransform(hProfile, TYPE_GRAY_8, hLab, TYPE_Lab_8, INTENT_RELATIVE_COLORIMETRIC, 0);
                if (hTransform2) {
                    unsigned char in2[1] = {0};
                    unsigned char out2[3] = {0, 0, 0};
                    cmsDoTransform(hTransform2, in2, out2, 1);
                    cmsDeleteTransform(hTransform2);
                }
            }
            cmsCloseProfile(hLab);
        }
        cmsCloseProfile(hProfile);
    } else {
        cmsHPROFILE hRgb = cmsCreate_sRGBProfile();
        if (hRgb) {
            cmsHPROFILE hGray = cmsCreateGrayProfile(cmsD50_xyY(), cmsBuildGamma(NULL, 2.2));
            if (hGray) {
                cmsHTRANSFORM hTransform = cmsCreateTransform(hRgb, TYPE_RGB_8, hGray, TYPE_GRAY_8, INTENT_PERCEPTUAL, 0);
                if (hTransform) {
                    unsigned char in[3] = {128, 128, 128};
                    unsigned char out[1] = {0};
                    cmsDoTransform(hTransform, in, out, 1);
                    cmsDeleteTransform(hTransform);
                }
                cmsCloseProfile(hGray);
            }
            cmsCloseProfile(hRgb);
        }
    }
    return 0;
}