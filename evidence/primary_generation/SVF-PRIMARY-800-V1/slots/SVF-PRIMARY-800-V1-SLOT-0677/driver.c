#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include <ares.h>

typedef struct {
    int done;
    int got_record;
} query_state;

static void query_callback(void *arg, int status, int timeouts, unsigned char *abuf, int alen) {
    (void)timeouts;
    (void)abuf;
    (void)alen;
    query_state *state = (query_state *)arg;
    if (status == ARES_SUCCESS) {
        state->got_record = 1;
    }
    state->done = 1;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 4) {
        return 0;
    }

    ares_channel channel;
    struct ares_options options;
    memset(&options, 0, sizeof(options));
    options.flags = ARES_FLAG_STAYOPEN;
    int optmask = ARES_OPT_FLAGS;

    if (ares_init_options(&channel, &options, optmask) != ARES_SUCCESS) {
        return 0;
    }

    const char *server_csv = getenv("SVF_CARES_SERVER_CSV");
    if (server_csv != NULL) {
        ares_set_servers_csv(channel, server_csv);
    }

    // Build a bounded hostname from fuzz input (max 63 chars per label, total 255)
    char hostname[256];
    size_t len = size < 255 ? size : 255;
    memcpy(hostname, data, len);
    hostname[len] = '\0';
    // Ensure it's a valid hostname-ish string: replace non-printable with 'a'
    for (size_t i = 0; i < len; i++) {
        if (hostname[i] < 33 || hostname[i] > 126) {
            hostname[i] = 'a';
        }
    }

    query_state state;
    state.done = 0;
    state.got_record = 0;

    ares_query_dnsrec(channel, hostname, ARES_CLASS_IN, ARES_REC_TYPE_A, query_callback, &state, NULL);

    // Process until done or timeout (bounded loop)
    int max_waits = 100;
    while (!state.done && max_waits-- > 0) {
        struct timeval tv;
        tv.tv_sec = 0;
        tv.tv_usec = 10000; // 10ms
        ares_process_fd(channel, ARES_SOCKET_BAD, ARES_SOCKET_BAD);
        select(0, NULL, NULL, NULL, &tv);
    }

    // Produce binary result: 1 if got_record, else 0
    uint8_t result = state.got_record ? 1 : 0;
    // Output via a simple side-effect to prevent optimization
    __asm__ volatile("" : : "r"(result) : "memory");

    ares_destroy(channel);
    return 0;
}