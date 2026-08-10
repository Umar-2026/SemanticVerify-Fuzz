#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include <ares.h>

typedef struct {
    int done;
    int status;
    struct ares_addrinfo *result;
} callback_data;

static void callback(void *arg, int status, int timeouts, struct ares_addrinfo *result) {
    callback_data *data = (callback_data *)arg;
    data->done = 1;
    data->status = status;
    data->result = result;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 4) {
        return 0;
    }

    ares_channel channel;
    struct ares_options options;
    memset(&options, 0, sizeof(options));

    /* Derive a bounded timeout from the first 4 bytes (0-1000 ms) */
    uint32_t raw_timeout;
    memcpy(&raw_timeout, data, 4);
    int timeout_ms = (int)(raw_timeout % 1001);
    options.timeout = timeout_ms;
    options.flags = ARES_FLAG_STAYOPEN;

    int status = ares_init_options(&channel, &options, ARES_OPT_TIMEOUT | ARES_OPT_FLAGS);
    if (status != ARES_SUCCESS) {
        return 0;
    }

    const char *server_csv = getenv("SVF_CARES_SERVER_CSV");
    if (server_csv != NULL) {
        ares_set_servers_csv(channel, server_csv);
    }

    /* Use remaining bytes to construct a hostname (bounded to 255 chars) */
    size_t name_len = size - 4;
    if (name_len > 255) {
        name_len = 255;
    }
    char *name = (char *)malloc(name_len + 1);
    if (name == NULL) {
        ares_destroy(channel);
        return 0;
    }
    memcpy(name, data + 4, name_len);
    name[name_len] = '\0';

    callback_data cb_data;
    memset(&cb_data, 0, sizeof(cb_data));

    struct ares_addrinfo_hints hints;
    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;

    ares_getaddrinfo(channel, name, NULL, &hints, callback, &cb_data);

    /* Process events until callback fires or a bounded number of iterations */
    int max_iterations = 100;
    while (!cb_data.done && max_iterations > 0) {
        ares_process_fd(channel, ARES_SOCKET_BAD, ARES_SOCKET_BAD);
        max_iterations--;
    }

    if (cb_data.result != NULL) {
        ares_freeaddrinfo(cb_data.result);
    }

    free(name);
    ares_destroy(channel);
    return 0;
}