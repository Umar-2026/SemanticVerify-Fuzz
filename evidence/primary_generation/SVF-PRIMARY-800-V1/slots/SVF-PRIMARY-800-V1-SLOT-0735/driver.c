#include <lcms2.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 8) return 0;

    // Extract parameters from the first bytes
    uint32_t input_format = 0;
    uint32_t output_format = 0;
    size_t offset = 0;

    // Use first 4 bytes for input format (little-endian)
    for (int i = 0; i < 4 && offset < size; i++) {
        input_format |= ((uint32_t)data[offset]) << (8 * i);
        offset++;
    }
    // Use next 4 bytes for output format
    for (int i = 0; i < 4 && offset < size; i++) {
        output_format |= ((uint32_t)data[offset]) << (8 * i);
        offset++;
    }

    // Remaining data is the pixel block
    size_t pixel_data_size = size - offset;
    if (pixel_data_size == 0) return 0;

    // Create a transform from sRGB to sRGB (simple identity-like transform)
    cmsHPROFILE srgb_profile = cmsCreate_sRGBProfile();
    if (!srgb_profile) return 0;

    cmsHTRANSFORM transform = cmsCreateTransform(
        srgb_profile, input_format,
        srgb_profile, output_format,
        INTENT_PERCEPTUAL, 0);
    cmsCloseProfile(srgb_profile);
    if (!transform) return 0;

    // Process the pixel data in chunks (e.g., up to 4096 pixels per call)
    // Determine the number of pixels per chunk based on input format
    // We'll just process the whole buffer if it's small, otherwise split.
    // For simplicity, we process the entire buffer in one call if it fits,
    // otherwise we split into chunks of 1024 bytes.
    const uint8_t *pixel_data = data + offset;
    size_t remaining = pixel_data_size;
    size_t chunk_size = 1024; // bytes per chunk
    uint8_t *output_buffer = NULL;

    // Allocate output buffer for the largest possible chunk
    // We'll allocate based on input chunk size and output format size.
    // Since we don't know exact sizes, we allocate a generous buffer.
    // For simplicity, we allocate a buffer of the same size as input chunk.
    output_buffer = (uint8_t *)malloc(chunk_size * 4); // generous
    if (!output_buffer) {
        cmsDeleteTransform(transform);
        return 0;
    }

    while (remaining > 0) {
        size_t current_chunk = remaining < chunk_size ? remaining : chunk_size;
        // Process the chunk
        cmsDoTransform(transform, (void *)pixel_data, output_buffer, current_chunk);
        pixel_data += current_chunk;
        remaining -= current_chunk;
    }

    free(output_buffer);
    cmsDeleteTransform(transform);
    return 0;
}