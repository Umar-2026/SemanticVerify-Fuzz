#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include "lcms2.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

    cmsHPROFILE hProfile = cmsOpenProfileFromMem(data, size);
    if (hProfile == NULL) return 0;

    // Inspect profile basic info
    cmsColorSpaceSignature colorSpace = cmsGetColorSpace(hProfile);
    cmsColorSpaceSignature pcs = cmsGetPCS(hProfile);
    cmsUInt32Number deviceClass = cmsGetDeviceClass(hProfile);
    cmsUInt32Number renditionIntent = cmsGetHeaderRenderingIntent(hProfile);
    cmsUInt32Number flags = cmsGetHeaderFlags(hProfile);
    cmsUInt32Number manufacturer = cmsGetHeaderManufacturer(hProfile);
    cmsUInt32Number model = cmsGetHeaderModel(hProfile);
    cmsUInt32Number creator = cmsGetHeaderCreator(hProfile);
    cmsUInt32Number profileID[4];
    cmsGetHeaderProfileID(hProfile, profileID);

    // Try to read a named color list if present
    cmsNAMEDCOLORLIST* namedColorList = cmsGetNamedColorList(hProfile);
    if (namedColorList != NULL) {
        cmsUInt32Number count = cmsNamedColorCount(namedColorList);
        for (cmsUInt32Number i = 0; i < count && i < 16; i++) {
            char name[256];
            char prefix[64];
            char suffix[64];
            cmsUInt16Number pcsCoords[3];
            cmsUInt16Number deviceCoords[16];
            if (cmsNamedColorInfo(namedColorList, i, name, prefix, suffix, pcsCoords, deviceCoords)) {
                // Just touch the data
                volatile cmsUInt16Number tmp = pcsCoords[0] + deviceCoords[0];
                (void)tmp;
            }
        }
    }

    // Try to create a transform from profile to Lab if it's an output or display profile
    if (deviceClass == cmsSigDisplayClass || deviceClass == cmsSigOutputClass) {
        cmsHPROFILE labProfile = cmsCreateLab4Profile(NULL);
        if (labProfile != NULL) {
            cmsHTRANSFORM hTransform = cmsCreateTransform(hProfile, TYPE_RGB_8, labProfile, TYPE_Lab_DBL, renditionIntent, flags);
            if (hTransform != NULL) {
                // Transform a small set of colors
                uint8_t rgb[3] = {0x80, 0x80, 0x80};
                double lab[3];
                cmsDoTransform(hTransform, rgb, lab, 1);
                cmsDeleteTransform(hTransform);
            }
            cmsCloseProfile(labProfile);
        }
    }

    // Try to save the profile to memory (round-trip)
    cmsUInt32Number bytesNeeded = 0;
    if (cmsSaveProfileToMem(hProfile, NULL, &bytesNeeded) && bytesNeeded > 0) {
        uint8_t *buffer = (uint8_t *)malloc(bytesNeeded);
        if (buffer != NULL) {
            cmsUInt32Number bytesWritten = 0;
            if (cmsSaveProfileToMem(hProfile, buffer, &bytesWritten)) {
                // Just touch the data
                volatile uint8_t sum = 0;
                for (cmsUInt32Number i = 0; i < bytesWritten && i < 64; i++) {
                    sum += buffer[i];
                }
                (void)sum;
            }
            free(buffer);
        }
    }

    cmsCloseProfile(hProfile);
    return 0;
}