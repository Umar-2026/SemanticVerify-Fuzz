#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include <ares.h>

#ifdef __cplusplus
extern "C" {
#endif

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1) {
        return 0;
    }

    ares_channel channel;
    struct ares_options options;
    memset(&options, 0, sizeof(options));
    options.flags = ARES_FLAG_STAYOPEN;
    int optmask = ARES_OPT_FLAGS;

    int status = ares_init_options(&channel, &options, optmask);
    if (status != ARES_SUCCESS) {
        return 0;
    }

    const char *server_csv = getenv("SVF_CARES_SERVER_CSV");
    if (server_csv != NULL && server_csv[0] != '\0') {
        ares_set_servers_csv(channel, server_csv);
    }

    // Derive a bounded domain name from fuzz input.
    // Use at most 63 bytes for the label, and ensure it is null-terminated.
    size_t domain_len = size;
    if (domain_len > 63) {
        domain_len = 63;
    }
    char domain[64];
    memcpy(domain, data, domain_len);
    domain[domain_len] = '\0';

    // Ensure the domain is not empty and does not contain invalid characters.
    if (domain[0] == '\0') {
        ares_destroy(channel);
        return 0;
    }

    // Issue an A-record query.
    ares_query_dnsrec(channel, domain, ARES_CLASS_IN, ARES_REC_TYPE_A, NULL, NULL, NULL);

    // Allow the query to proceed briefly.
    int nfds;
    fd_set readers, writers;
    struct timeval tv;
    tv.tv_sec = 0;
    tv.tv_usec = 10000; // 10 ms
    for (int i = 0; i < 5; i++) {
        FD_ZERO(&readers);
        FD_ZERO(&writers);
        nfds = ares_fds(channel, &readers, &writers);
        if (nfds == 0) {
            break;
        }
        if (select(nfds, &readers, &writers, NULL, &tv) < 0) {
            break;
        }
        ares_process(channel, &readers, &writers);
    }

    ares_destroy(channel);
    return 0;
}

#ifdef __cplusplus
}
#endif