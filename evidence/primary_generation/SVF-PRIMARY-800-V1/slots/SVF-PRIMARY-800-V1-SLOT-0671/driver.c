#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include <ares.h>

typedef struct {
    int done;
    int got_record;
} query_state;

static void query_callback(void *arg, int status, int timeouts, ares_dns_record_t *dnsrec) {
    query_state *state = (query_state *)arg;
    (void)timeouts;
    if (status == ARES_SUCCESS && dnsrec != NULL) {
        state->got_record = 1;
    }
    state->done = 1;
    ares_dns_record_destroy(dnsrec);
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 1) {
        return 0;
    }

    const char *server_csv = getenv("SVF_CARES_SERVER_CSV");
    if (server_csv == NULL || server_csv[0] == '\0') {
        return 0;
    }

    ares_channel_t *channel = NULL;
    struct ares_options options;
    memset(&options, 0, sizeof(options));
    options.flags = ARES_FLAG_STAYOPEN;

    if (ares_init_options(&channel, &options, 0) != ARES_SUCCESS) {
        return 0;
    }

    if (ares_set_servers_csv(channel, server_csv) != ARES_SUCCESS) {
        ares_destroy(channel);
        return 0;
    }

    // Build a bounded hostname from fuzz input (max 63 chars per DNS label, total <= 255)
    char name[256];
    size_t name_len = size < sizeof(name) - 1 ? size : sizeof(name) - 1;
    memcpy(name, data, name_len);
    name[name_len] = '\0';

    // Ensure the name is a valid hostname: replace invalid characters with 'a'
    for (size_t i = 0; i < name_len; i++) {
        char c = name[i];
        if (!((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') ||
              (c >= '0' && c <= '9') || c == '-' || c == '.')) {
            name[i] = 'a';
        }
    }

    query_state state;
    state.done = 0;
    state.got_record = 0;

    ares_query_dnsrec(channel, name, ARES_CLASS_IN, ARES_REC_TYPE_A, query_callback, &state, NULL);

    // Process the event loop until the query completes or a reasonable timeout
    int max_waits = 1000;
    while (!state.done && max_waits-- > 0) {
        ares_queue_wait(channel, 1000);
        ares_process_fd(channel, ARES_SOCKET_BAD, ARES_SOCKET_BAD);
    }

    // The result is implicitly captured in state.got_record; we just need to ensure cleanup.
    ares_destroy(channel);

    return 0;
}