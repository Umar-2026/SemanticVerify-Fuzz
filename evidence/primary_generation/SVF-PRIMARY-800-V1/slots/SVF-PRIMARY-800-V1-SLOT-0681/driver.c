#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <stddef.h>
#include <ares.h>

#ifdef __cplusplus
extern "C" {
#endif

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1) return 0;

    const char *server_csv = getenv("SVF_CARES_SERVER_CSV");
    if (!server_csv) server_csv = "127.0.0.1";

    ares_channel channel;
    struct ares_options options;
    memset(&options, 0, sizeof(options));
    int optmask = 0;

    int status = ares_init_options(&channel, &options, optmask);
    if (status != ARES_SUCCESS) {
        return 0;
    }

    status = ares_set_servers_csv(channel, server_csv);
    if (status != ARES_SUCCESS) {
        ares_destroy(channel);
        return 0;
    }

    char name[256];
    size_t name_len = size < sizeof(name) - 1 ? size : sizeof(name) - 1;
    memcpy(name, data, name_len);
    name[name_len] = '\0';

    ares_getaddrinfo(channel, name, NULL, NULL, NULL, NULL);

    ares_destroy(channel);
    return 0;
}

#ifdef __cplusplus
}
#endif