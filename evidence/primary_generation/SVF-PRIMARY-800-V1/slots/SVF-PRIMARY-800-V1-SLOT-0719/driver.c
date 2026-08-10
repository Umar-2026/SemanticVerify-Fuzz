#include "lcms2.h"
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

#define MAX_INPUT_SIZE 4096

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 8 || size > MAX_INPUT_SIZE) {
        return 0;
    }

    // Extract bounded parameters from the first bytes
    uint32_t intent = data[0] % 4;          // 0..3
    uint32_t input_format = data[1] % 8;    // 0..7
    uint32_t output_format = data[2] % 8;   // 0..7
    uint32_t flags = data[3] & 0x03;        // 0..3

    // Determine pixel size based on format (simplified: 3 or 4 channels, 8 or 16 bits)
    size_t input_pixel_size = 3 * sizeof(uint8_t);
    size_t output_pixel_size = 3 * sizeof(uint8_t);
    if (input_format & 0x04) input_pixel_size = 4 * sizeof(uint8_t);
    if (input_format & 0x02) input_pixel_size = 3 * sizeof(uint16_t);
    if (input_format & 0x06) input_pixel_size = 4 * sizeof(uint16_t);
    if (output_format & 0x04) output_pixel_size = 4 * sizeof(uint8_t);
    if (output_format & 0x02) output_pixel_size = 3 * sizeof(uint16_t);
    if (output_format & 0x06) output_pixel_size = 4 * sizeof(uint16_t);

    // Use remaining data as pixel data (at least one pixel)
    size_t available = size - 4;
    if (available < input_pixel_size) {
        return 0;
    }
    size_t num_pixels = available / input_pixel_size;
    if (num_pixels == 0) {
        return 0;
    }

    // Create a simple RGB profile (sRGB) for input and output
    cmsHPROFILE input_profile = cmsCreate_sRGBProfile();
    cmsHPROFILE output_profile = cmsCreate_sRGBProfile();
    if (!input_profile || !output_profile) {
        if (input_profile) cmsCloseProfile(input_profile);
        if (output_profile) cmsCloseProfile(output_profile);
        return 0;
    }

    // Create transform
    cmsHTRANSFORM transform = cmsCreateTransform(
        input_profile,
        input_format,
        output_profile,
        output_format,
        intent,
        flags
    );
    if (!transform) {
        cmsCloseProfile(input_profile);
        cmsCloseProfile(output_profile);
        return 0;
    }

    // Prepare output buffer
    size_t output_size = num_pixels * output_pixel_size;
    uint8_t *output_buffer = (uint8_t *)malloc(output_size);
    if (!output_buffer) {
        cmsDeleteTransform(transform);
        cmsCloseProfile(input_profile);
        cmsCloseProfile(output_profile);
        return 0;
    }

    // Process pixel data
    const uint8_t *input_data = data + 4;
    cmsDoTransform(transform, input_data, output_buffer, num_pixels);

    // Cleanup
    free(output_buffer);
    cmsDeleteTransform(transform);
    cmsCloseProfile(input_profile);
    cmsCloseProfile(output_profile);

    return 0;
}