#include "lcms2.h"
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 4) {
        return 0;
    }

    cmsHPROFILE hProfile = cmsOpenProfileFromMem(data, size);
    if (hProfile == NULL) {
        return 0;
    }

    // Inspect basic profile information
    cmsInfoType infoType = cmsInfoDescription;
    char buffer[256];
    cmsGetProfileInfoASCII(hProfile, infoType, "en", "US", buffer, sizeof(buffer));

    infoType = cmsInfoManufacturer;
    cmsGetProfileInfoASCII(hProfile, infoType, "en", "US", buffer, sizeof(buffer));

    infoType = cmsInfoModel;
    cmsGetProfileInfoASCII(hProfile, infoType, "en", "US", buffer, sizeof(buffer));

    infoType = cmsInfoCopyright;
    cmsGetProfileInfoASCII(hProfile, infoType, "en", "US", buffer, sizeof(buffer));

    // Get color space and PCS
    cmsColorSpaceSignature colorSpace = cmsGetColorSpace(hProfile);
    cmsColorSpaceSignature pcs = cmsGetPCS(hProfile);

    // Get device class
    cmsProfileClassSignature deviceClass = cmsGetDeviceClass(hProfile);

    // Get rendering intent
    cmsUInt32Number renderingIntent = cmsGetHeaderRenderingIntent(hProfile);

    // Get profile flags
    cmsUInt32Number flags = cmsGetHeaderFlags(hProfile);

    // Get manufacturer and model from header
    cmsUInt32Number manufacturer = cmsGetHeaderManufacturer(hProfile);
    cmsUInt32Number model = cmsGetHeaderModel(hProfile);

    // Get creation date/time
    struct tm creationTime;
    cmsGetHeaderCreationDateTime(hProfile, &creationTime);

    // Get profile ID
    cmsUInt8Number profileID[16];
    cmsGetHeaderProfileID(hProfile, profileID);

    // Get version
    cmsFloat64Number version = cmsGetProfileVersion(hProfile);

    // Get encoding of the profile
    cmsUInt32Number encoding = cmsGetEncodedICCversion(hProfile);

    // Get tag count and iterate over tags
    cmsUInt32Number tagCount = cmsGetTagCount(hProfile);
    for (cmsUInt32Number i = 0; i < tagCount; i++) {
        cmsTagSignature sig = cmsGetTagSignature(hProfile, i);
        if (cmsIsTag(hProfile, sig)) {
            cmsUInt32Number tagSize = 0;
            cmsUInt32Number tagType = 0;
            cmsReadRawTag(hProfile, sig, NULL, &tagSize, &tagType);
            if (tagSize > 0 && tagSize < 1024 * 1024) {
                void *tagData = malloc(tagSize);
                if (tagData) {
                    cmsReadRawTag(hProfile, sig, tagData, &tagSize, &tagType);
                    free(tagData);
                }
            }
        }
    }

    // Get profile description (may be localized)
    cmsMLU *mlu = (cmsMLU *)cmsReadTag(hProfile, cmsSigProfileDescriptionTag);
    if (mlu) {
        cmsUInt32Number len = cmsMLUgetASCII(mlu, "en", "US", NULL, 0);
        if (len > 0 && len < sizeof(buffer)) {
            cmsMLUgetASCII(mlu, "en", "US", buffer, sizeof(buffer));
        }
    }

    // Get copyright tag
    cmsMLU *copyright = (cmsMLU *)cmsReadTag(hProfile, cmsSigCopyrightTag);
    if (copyright) {
        cmsUInt32Number len = cmsMLUgetASCII(copyright, "en", "US", NULL, 0);
        if (len > 0 && len < sizeof(buffer)) {
            cmsMLUgetASCII(copyright, "en", "US", buffer, sizeof(buffer));
        }
    }

    // Get white point
    cmsCIEXYZ whitePoint;
    if (cmsReadTag(hProfile, cmsSigMediaWhitePointTag)) {
        cmsCIEXYZ *wp = (cmsCIEXYZ *)cmsReadTag(hProfile, cmsSigMediaWhitePointTag);
        if (wp) {
            whitePoint = *wp;
        }
    }

    // Get chromatic adaptation tag if present
    if (cmsIsTag(hProfile, cmsSigChromaticAdaptationTag)) {
        cmsCIEXYZ *adaptation = (cmsCIEXYZ *)cmsReadTag(hProfile, cmsSigChromaticAdaptationTag);
        if (adaptation) {
            // Just read it
        }
    }

    // Get A2B0 tag if present (for devicelink profiles)
    if (cmsIsTag(hProfile, cmsSigAToB0Tag)) {
        cmsHTRANSFORM transform = cmsCreateTransform(hProfile, TYPE_RGB_8, hProfile, TYPE_RGB_8, INTENT_PERCEPTUAL, 0);
        if (transform) {
            cmsUInt8Number in[3] = {128, 128, 128};
            cmsUInt8Number out[3] = {0, 0, 0};
            cmsDoTransform(transform, in, out, 1);
            cmsDeleteTransform(transform);
        }
    }

    // Get B2A0 tag if present
    if (cmsIsTag(hProfile, cmsSigBToA0Tag)) {
        cmsHTRANSFORM transform = cmsCreateTransform(hProfile, TYPE_RGB_8, hProfile, TYPE_RGB_8, INTENT_PERCEPTUAL, 0);
        if (transform) {
            cmsUInt8Number in[3] = {128, 128, 128};
            cmsUInt8Number out[3] = {0, 0, 0};
            cmsDoTransform(transform, in, out, 1);
            cmsDeleteTransform(transform);
        }
    }

    // Get gamut tag if present
    if (cmsIsTag(hProfile, cmsSigGamutTag)) {
        cmsHTRANSFORM transform = cmsCreateTransform(hProfile, TYPE_RGB_8, hProfile, TYPE_RGB_8, INTENT_PERCEPTUAL, 0);
        if (transform) {
            cmsUInt8Number in[3] = {128, 128, 128};
            cmsUInt8Number out[3] = {0, 0, 0};
            cmsDoTransform(transform, in, out, 1);
            cmsDeleteTransform(transform);
        }
    }

    // Get DToB0 tag if present
    if (cmsIsTag(hProfile, cmsSigDToB0Tag)) {
        cmsHTRANSFORM transform = cmsCreateTransform(hProfile, TYPE_RGB_8, hProfile, TYPE_RGB_8, INTENT_PERCEPTUAL, 0);
        if (transform) {
            cmsUInt8Number in[3] = {128, 128, 128};
            cmsUInt8Number out[3] = {0, 0, 0};
            cmsDoTransform(transform, in, out, 1);
            cmsDeleteTransform(transform);
        }
    }

    // Get BToD0 tag if present
    if (cmsIsTag(hProfile, cmsSigBToD0Tag)) {
        cmsHTRANSFORM transform = cmsCreateTransform(hProfile, TYPE_RGB_8, hProfile, TYPE_RGB_8, INTENT_PERCEPTUAL, 0);
        if (transform) {
            cmsUInt8Number in[3] = {128, 128, 128};
            cmsUInt8Number out[3] = {0, 0, 0};
            cmsDoTransform(transform, in, out, 1);
            cmsDeleteTransform(transform);
        }
    }

    // Get DToB1 tag if present
    if (cmsIsTag(hProfile, cmsSigDToB1Tag)) {
        cmsHTRANSFORM transform = cmsCreateTransform(hProfile, TYPE_RGB_8, hProfile, TYPE_RGB_8, INTENT_PERCEPTUAL, 0);
        if (transform) {
            cmsUInt8Number in[3] = {128, 128, 128};
            cmsUInt8Number out[3] = {0, 0, 0};
            cmsDoTransform(transform, in, out, 1);
            cmsDeleteTransform(transform);
        }
    }

    // Get BToD1 tag if present
    if (cmsIsTag(hProfile, cmsSigBToD1Tag)) {
        cmsHTRANSFORM transform = cmsCreateTransform(hProfile, TYPE_RGB_8, hProfile, TYPE_RGB_8, INTENT_PERCEPTUAL, 0);
        if (transform) {
            cmsUInt8Number in[3] = {128, 128, 128};
            cmsUInt8Number out[3] = {0, 0, 0};
            cmsDoTransform(transform, in, out, 1);
            cmsDeleteTransform(transform);
        }
    }

    // Get DToB2 tag if present
    if (cmsIsTag(hProfile, cmsSigDToB2Tag)) {
        cmsHTRANSFORM transform = cmsCreateTransform(hProfile, TYPE_RGB_8, hProfile, TYPE_RGB_8, INTENT_PERCEPTUAL, 0);
        if (transform) {
            cmsUInt8Number in[3] = {128, 128, 128};
            cmsUInt8Number out[3] = {0, 0, 0};
            cmsDoTransform(transform, in, out, 1);
            cmsDeleteTransform(transform);
        }
    }

    // Get BToD2 tag if present
    if (cmsIsTag(hProfile, cmsSigBToD2Tag)) {
        cmsHTRANSFORM transform = cmsCreateTransform(hProfile, TYPE_RGB_8, hProfile, TYPE_RGB_8, INTENT_PERCEPTUAL, 0);
        if (transform) {
            cmsUInt8Number in[3] = {128, 128, 128};
            cmsUInt8Number out[3] = {0, 0, 0};
            cmsDoTransform(transform, in, out, 1);
            cmsDeleteTransform(transform);
        }
    }

    // Get DToB3 tag if present
    if (cmsIsTag(hProfile, cmsSigDToB3Tag)) {
        cmsHTRANSFORM transform = cmsCreateTransform(hProfile, TYPE_RGB_8, hProfile, TYPE_RGB_8, INTENT_PERCEPTUAL, 0);
        if (transform) {
            cmsUInt8Number in[3] = {128, 128, 128};
            cmsUInt8Number out[3] = {0, 0, 0};
            cmsDoTransform(transform, in, out, 1);
            cmsDeleteTransform(transform);
        }
    }

    // Get BToD3 tag if present
    if (cmsIsTag(hProfile, cmsSigBToD3Tag)) {
        cmsHTRANSFORM transform = cmsCreateTransform(hProfile, TYPE_RGB_8, hProfile, TYPE_RGB_8, INTENT_PERCEPTUAL, 0);
        if (transform) {
            cmsUInt8Number in[3] = {128, 128, 128};
            cmsUInt8Number out[3] = {0, 0, 0};
            cmsDoTransform(transform, in, out, 1);
            cmsDeleteTransform(transform);
        }
    }

    // Get A2B1 tag if present
    if (cmsIsTag(hProfile, cmsSigAToB1Tag)) {
        cmsHTRANSFORM transform = cmsCreateTransform(hProfile, TYPE_RGB_8, hProfile, TYPE_RGB_8, INTENT_RELATIVE_COLORIMETRIC, 0);
        if (transform) {
            cmsUInt8Number in[3] = {128, 128, 128};
            cmsUInt8Number out[3] = {0, 0, 0};
            cmsDoTransform(transform, in, out, 1);
            cmsDeleteTransform(transform);
        }
    }

    // Get A2B2 tag if present
    if (cmsIsTag(hProfile, cmsSigAToB2Tag)) {
        cmsHTRANSFORM transform = cmsCreateTransform(hProfile, TYPE_RGB_8, hProfile, TYPE_RGB_8, INTENT_SATURATION, 0);
        if (transform) {
            cmsUInt8Number in[3] = {128, 128, 128};
            cmsUInt8Number out[3] = {0, 0, 0};
            cmsDoTransform(transform, in, out, 1);
            cmsDeleteTransform(transform);
        }
    }

    // Get A2B3 tag if present
    if (cmsIsTag(hProfile, cmsSigAToB3Tag)) {
        cmsHTRANSFORM transform = cmsCreateTransform(hProfile, TYPE_RGB_8, hProfile, TYPE_RGB_8, INTENT_ABSOLUTE_COLORIMETRIC, 0);
        if (transform) {
            cmsUInt8Number in[3] = {128, 128, 128};
            cmsUInt8Number out[3] = {0, 0, 0};
            cmsDoTransform(transform, in, out, 1);
            cmsDeleteTransform(transform);
        }
    }

    // Get B2A1 tag if present
    if (cmsIsTag(hProfile, cmsSigBToA1Tag)) {
        cmsHTRANSFORM transform = cmsCreateTransform(hProfile, TYPE_RGB_8, hProfile, TYPE_RGB_8, INTENT_RELATIVE_COLORIMETRIC, 0);
        if (transform) {
            cmsUInt8Number in[3] = {128, 128, 128};
            cmsUInt8Number out[3] = {0, 0, 0};
            cmsDoTransform(transform, in, out, 1);
            cmsDeleteTransform(transform);
        }
    }

    // Get B2A2 tag if present
    if (cmsIsTag(hProfile, cmsSigBToA2Tag)) {
        cmsHTRANSFORM transform = cmsCreateTransform(hProfile, TYPE_RGB_8, hProfile, TYPE_RGB_8, INTENT_SATURATION, 0);
        if (transform) {
            cmsUInt8Number in[3] = {128, 128, 128};
            cmsUInt8Number out[3] = {0, 0, 0};
            cmsDoTransform(transform, in, out, 1);
            cmsDeleteTransform(transform);
        }
    }

    // Get B2A3 tag if present
    if (cmsIsTag(hProfile, cmsSigBToA3Tag)) {
        cmsHTRANSFORM transform = cmsCreateTransform(hProfile, TYPE_RGB_8, hProfile, TYPE_RGB_8, INTENT_ABSOLUTE_COLORIMETRIC, 0);
        if (transform) {
            cmsUInt8Number in[3] = {128, 128, 128};
            cmsUInt8Number out[3] = {0, 0, 0};
            cmsDoTransform(transform, in, out, 1);
            cmsDeleteTransform(transform);
        }
    }

    // Get profile sequence description if present
    if (cmsIsTag(hProfile, cmsSigProfileSequenceDescTag)) {
        cmsSEQ *seq = (cmsSEQ *)cmsReadTag(hProfile, cmsSigProfileSequenceDescTag);
        if (seq) {
            // Just read it
        }
    }

    // Get viewing conditions if present
    if (cmsIsTag(hProfile, cmsSigViewingConditionsTag)) {
        cmsICCViewingConditions *vc = (cmsICCViewingConditions *)cmsReadTag(hProfile, cmsSigViewingConditionsTag);
        if (vc) {
            // Just read it
        }
    }

    // Get named color list if present
    if (cmsIsTag(hProfile, cmsSigNamedColor2Tag)) {
        cmsNAMEDCOLORLIST *nc = (cmsNAMEDCOLORLIST *)cmsReadTag(hProfile, cmsSigNamedColor2Tag);
        if (nc) {
            cmsUInt32Number count = cmsNamedColorCount(nc);
            for (cmsUInt32Number i = 0; i < count && i < 10; i++) {
                char name[256];
                cmsNamedColorInfo(nc, i, name, NULL, NULL, NULL, NULL);
            }
        }
    }

    // Get calibration table if present
    if (cmsIsTag(hProfile, cmsSigCalibrationDateTimeTag)) {
        cmsDateTimeNumber *dt = (cmsDateTimeNumber *)cmsReadTag(hProfile, cmsSigCalibrationDateTimeTag);
        if (dt) {
            // Just read it
        }
    }

    // Get chromaticity if present
    if (cmsIsTag(hProfile, cmsSigChromaticityTag)) {
        cmsCIExyY *chrom = (cmsCIExyY *)cmsReadTag(hProfile, cmsSigChromaticityTag);
        if (chrom) {
            // Just read it
        }
    }

    // Get colorant order if present
    if (cmsIsTag(hProfile, cmsSigColorantOrderTag)) {
        cmsUInt8Number *order = (cmsUInt8Number *)cmsReadTag(hProfile, cmsSigColorantOrderTag);
        if (order) {
            // Just read it
        }
    }

    // Get colorant table if present
    if (cmsIsTag(hProfile, cmsSigColorantTableTag)) {
        cmsUInt16Number *table = (cmsUInt16Number *)cmsReadTag(hProfile, cmsSigColorantTableTag);
        if (table) {
            // Just read it
        }
    }

    // Get device settings if present
    if (cmsIsTag(hProfile, cmsSigDeviceSettingsTag)) {
        cmsUInt8Number *settings = (cmsUInt8Number *)cmsReadTag(hProfile, cmsSigDeviceSettingsTag);
        if (settings) {
            // Just read it
        }
    }

    // Get gamut boundary description if present
    if (cmsIsTag(hProfile, cmsSigGamutBoundaryDescriptionTag)) {
        cmsGDB *gdb = (cmsGDB *)cmsReadTag(hProfile, cmsSigGamutBoundaryDescriptionTag);
        if (gdb) {
            // Just read it
        }
    }

    // Get measurement if present
    if (cmsIsTag(hProfile, cmsSigMeasurementTag)) {
        cmsICCMeasurementConditions *mc = (cmsICCMeasurementConditions *)cmsReadTag(hProfile, cmsSigMeasurementTag);
        if (mc) {
            // Just read it
        }
    }

    // Get technology if present
    if (cmsIsTag(hProfile, cmsSigTechnologyTag)) {
        cmsTechnologySignature tech = *(cmsTechnologySignature *)cmsReadTag(hProfile, cmsSigTechnologyTag);
        // Just read it
    }

    // Get UCRBG if present
    if (cmsIsTag(hProfile, cmsSigUcrBgTag)) {
        cmsUcrBg *ucrbg = (cmsUcrBg *)cmsReadTag(hProfile, cmsSigUcrBgTag);
        if (ucrbg) {
            // Just read it
        }
    }

    // Get VCGT if present
    if (cmsIsTag(hProfile, cmsSigVcgtTag)) {
        cmsToneCurve **vcgt = (cmsToneCurve **)cmsReadTag(hProfile, cmsSigVcgtTag);
        if (vcgt) {
            // Just read it
        }
    }

    // Get DToB0 tag if present (already done above, but keep for completeness)
    // Get BToD0 tag if present (already done above)

    // Get profile ID (already done above)

    // Get profile description (already done above)

    // Get copyright (already done above)

    // Get manufacturer (already done above)

    // Get model (already done above)

    // Get creation date (already done above)

    // Get version (already done above)

    // Get encoding (already done above)

    // Get flags (already done above)

    // Get rendering intent (already done above)

    // Get device class (already done above)

    // Get color space (already done above)

    // Get PCS (already done above)

    // Get white point (already done above)

    // Get chromatic adaptation (already done above)

    // Get A2B0 (already done above)

    // Get B2A0 (already done above)

    // Get gamut (already done above)

    // Get DToB0 (already done above)

    // Get BToD0 (already done above)

    // Get DToB1 (already done above)

    // Get BToD1 (already done above)

    // Get DToB2 (already done above)

    // Get BToD2 (already done above)

    // Get DToB3 (already done above)

    // Get BToD3 (already done above)

    // Get A2B1 (already done above)

    // Get A2B2 (already done above)

    // Get A2B3 (already done above)

    // Get B2A1 (already done above)

    // Get B2A2 (already done above)

    // Get B2A3 (already done above)

    // Get profile sequence description (already done above)

    // Get viewing conditions (already done above)

    // Get named color list (already done above)

    // Get calibration date/time (already done above)

    // Get chromaticity (already done above)

    // Get colorant order (already done above)

    // Get colorant table (already done above)

    // Get device settings (already done above)

    // Get gamut boundary description (already done above)

    // Get measurement (already done above)

    // Get technology (already done above)

    // Get UCRBG (already done above)

    // Get VCGT (already done above)

    // Close the profile
    cmsCloseProfile(hProfile);

    return 0;
}