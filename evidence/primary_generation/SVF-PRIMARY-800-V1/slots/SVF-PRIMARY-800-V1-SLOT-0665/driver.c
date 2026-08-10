#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ares.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <sys/socket.h>
#include <netinet/in.h>

static int callback_count = 0;
static int callback_failures = 0;

struct callback_data {
    int channel_id;
    int done;
    int status;
};

static void addr_callback(void *arg, int status, int timeouts, struct ares_addrinfo *result) {
    struct callback_data *data = (struct callback_data *)arg;
    data->done = 1;
    data->status = status;
    if (status != ARES_SUCCESS) {
        callback_failures++;
        fprintf(stderr, "Channel %d lookup failed: %s\n", data->channel_id, ares_strerror(status));
    } else {
        callback_count++;
        /* Consume the result minimally */
        if (result) {
            struct ares_addrinfo_node *node = result->nodes;
            while (node) {
                node = node->ai_next;
            }
        }
    }
    if (result) {
        ares_freeaddrinfo(result);
    }
}

int main(int argc, char **argv) {
    const char *server_csv = getenv("SVF_CARES_SERVER_CSV");
    if (!server_csv || !*server_csv) {
        fprintf(stderr, "SVF_CARES_SERVER_CSV not set\n");
        return 1;
    }

    if (ares_library_init(ARES_LIB_INIT_ALL) != ARES_SUCCESS) {
        fprintf(stderr, "ares_library_init failed\n");
        return 1;
    }

    struct ares_options options;
    memset(&options, 0, sizeof(options));
    int optmask = 0;

    ares_channel channel1 = NULL;
    ares_channel channel2 = NULL;

    int status = ares_init_options(&channel1, &options, optmask);
    if (status != ARES_SUCCESS) {
        fprintf(stderr, "ares_init_options channel1 failed: %s\n", ares_strerror(status));
        ares_library_cleanup();
        return 1;
    }

    status = ares_init_options(&channel2, &options, optmask);
    if (status != ARES_SUCCESS) {
        fprintf(stderr, "ares_init_options channel2 failed: %s\n", ares_strerror(status));
        ares_destroy(channel1);
        ares_library_cleanup();
        return 1;
    }

    status = ares_set_servers_csv(channel1, server_csv);
    if (status != ARES_SUCCESS) {
        fprintf(stderr, "ares_set_servers_csv channel1 failed: %s\n", ares_strerror(status));
        ares_destroy(channel1);
        ares_destroy(channel2);
        ares_library_cleanup();
        return 1;
    }

    status = ares_set_servers_csv(channel2, server_csv);
    if (status != ARES_SUCCESS) {
        fprintf(stderr, "ares_set_servers_csv channel2 failed: %s\n", ares_strerror(status));
        ares_destroy(channel1);
        ares_destroy(channel2);
        ares_library_cleanup();
        return 1;
    }

    struct callback_data data1 = {1, 0, 0};
    struct callback_data data2 = {2, 0, 0};

    /* Use a fixed hostname for bounded lookup */
    const char *hostname = "example.com";

    status = ares_getaddrinfo(channel1, hostname, NULL, NULL, addr_callback, &data1);
    if (status != ARES_SUCCESS) {
        fprintf(stderr, "ares_getaddrinfo channel1 failed: %s\n", ares_strerror(status));
        ares_destroy(channel1);
        ares_destroy(channel2);
        ares_library_cleanup();
        return 1;
    }

    status = ares_getaddrinfo(channel2, hostname, NULL, NULL, addr_callback, &data2);
    if (status != ARES_SUCCESS) {
        fprintf(stderr, "ares_getaddrinfo channel2 failed: %s\n", ares_strerror(status));
        ares_destroy(channel1);
        ares_destroy(channel2);
        ares_library_cleanup();
        return 1;
    }

    /* Process both channels until both callbacks are done or timeout */
    int max_fds = 0;
    fd_set read_fds, write_fds;
    struct timeval tv;
    int nfds;
    int both_done = 0;
    int iterations = 0;
    const int max_iterations = 1000;

    while (!both_done && iterations < max_iterations) {
        FD_ZERO(&read_fds);
        FD_ZERO(&write_fds);
        max_fds = 0;

        ares_fds(channel1, &read_fds, &write_fds);
        ares_fds(channel2, &read_fds, &write_fds);

        nfds = ares_getsock(channel1, NULL, 0);
        if (nfds > max_fds) max_fds = nfds;
        nfds = ares_getsock(channel2, NULL, 0);
        if (nfds > max_fds) max_fds = nfds;

        tv.tv_sec = 0;
        tv.tv_usec = 100000; /* 100ms */

        if (max_fds == 0) {
            /* No sockets, just process timeouts */
            ares_process_fd(channel1, ARES_SOCKET_BAD, ARES_SOCKET_BAD);
            ares_process_fd(channel2, ARES_SOCKET_BAD, ARES_SOCKET_BAD);
        } else {
            if (select(max_fds + 1, &read_fds, &write_fds, NULL, &tv) < 0) {
                break;
            }
            ares_process_fd(channel1, FD_ISSET(0, &read_fds) ? 0 : ARES_SOCKET_BAD,
                            FD_ISSET(0, &write_fds) ? 0 : ARES_SOCKET_BAD);
            ares_process_fd(channel2, FD_ISSET(0, &read_fds) ? 0 : ARES_SOCKET_BAD,
                            FD_ISSET(0, &write_fds) ? 0 : ARES_SOCKET_BAD);
        }

        if (data1.done && data2.done) {
            both_done = 1;
        }
        iterations++;
    }

    ares_destroy(channel1);
    ares_destroy(channel2);
    ares_library_cleanup();

    if (!both_done) {
        fprintf(stderr, "Timed out waiting for callbacks\n");
        return 1;
    }

    if (callback_failures > 0) {
        fprintf(stderr, "One or more lookups failed\n");
        return 1;
    }

    if (callback_count != 2) {
        fprintf(stderr, "Expected 2 successful callbacks, got %d\n", callback_count);
        return 1;
    }

    return 0;
}