#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <ares.h>

#ifdef SVF_CARES_SERVER_CSV
static const char *server_csv = SVF_CARES_SERVER_CSV;
#else
static const char *server_csv = "127.0.0.1";
#endif

typedef struct {
    int query_id;
    int done;
    int status;
    unsigned char *addr;
    size_t addr_len;
} query_result_t;

static void a_callback(void *arg, int status, int timeouts, unsigned char *abuf, int alen) {
    (void)timeouts;
    query_result_t *res = (query_result_t *)arg;
    res->status = status;
    res->done = 1;
    if (status == ARES_SUCCESS && abuf != NULL) {
        struct ares_dns_record *dnsrec = NULL;
        ares_status_t rv = ares_dns_parse(abuf, (size_t)alen, 0, &dnsrec);
        if (rv == ARES_SUCCESS && dnsrec != NULL) {
            size_t n_an = ares_dns_record_rr_cnt(dnsrec, ARES_SECTION_ANSWER);
            for (size_t i = 0; i < n_an; i++) {
                const struct ares_dns_rr *rr = ares_dns_record_rr_get(dnsrec, ARES_SECTION_ANSWER, i);
                if (rr == NULL) continue;
                if (ares_dns_rr_get_type(rr) == ARES_REC_TYPE_A) {
                    const unsigned char *addr = ares_dns_rr_get_addr(rr, ARES_RR_ADDR);
                    if (addr != NULL) {
                        res->addr = (unsigned char *)malloc(4);
                        if (res->addr) {
                            memcpy(res->addr, addr, 4);
                            res->addr_len = 4;
                        }
                    }
                    break;
                }
            }
            ares_dns_record_destroy(dnsrec);
        }
    }
    if (abuf != NULL) {
        ares_free_string(abuf);
    }
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 2) return 0;

    // Derive two bounded hostnames from fuzz input.
    // We'll use up to 63 bytes each for the labels, and ensure they are valid hostname characters.
    char name1[64];
    char name2[64];
    size_t len1 = (size_t)(data[0] % 63) + 1; // 1..63
    size_t len2 = (size_t)(data[1] % 63) + 1;
    if (size < 2 + len1 + len2) return 0;

    size_t pos = 2;
    for (size_t i = 0; i < len1; i++) {
        unsigned char c = data[pos + i];
        // Map to [a-z0-9-] to keep valid hostname
        if (c % 27 == 26) {
            name1[i] = '-';
        } else {
            name1[i] = (char)('a' + (c % 26));
        }
    }
    name1[len1] = '\0';
    pos += len1;

    for (size_t i = 0; i < len2; i++) {
        unsigned char c = data[pos + i];
        if (c % 27 == 26) {
            name2[i] = '-';
        } else {
            name2[i] = (char)('a' + (c % 26));
        }
    }
    name2[len2] = '\0';

    ares_channel_t channel;
    struct ares_options options;
    memset(&options, 0, sizeof(options));
    options.flags = ARES_FLAG_STAYOPEN;
    options.timeout = 2000;
    options.tries = 1;

    ares_status_t status = ares_init_options(&channel, &options, ARES_OPT_FLAGS | ARES_OPT_TIMEOUT | ARES_OPT_TRIES);
    if (status != ARES_SUCCESS) {
        return 0;
    }

    status = ares_set_servers_csv(channel, server_csv);
    if (status != ARES_SUCCESS) {
        ares_destroy(channel);
        return 0;
    }

    query_result_t res1 = {0};
    query_result_t res2 = {0};
    res1.query_id = 1;
    res2.query_id = 2;

    struct ares_dns_record *dnsrec1 = NULL;
    struct ares_dns_record *dnsrec2 = NULL;

    status = ares_dns_record_create(&dnsrec1, 0, ARES_OPCODE_QUERY, ARES_RCODE_NOERROR);
    if (status != ARES_SUCCESS) {
        ares_destroy(channel);
        return 0;
    }
    status = ares_dns_record_add_query(dnsrec1, name1, ARES_CLASS_IN, ARES_REC_TYPE_A);
    if (status != ARES_SUCCESS) {
        ares_dns_record_destroy(dnsrec1);
        ares_destroy(channel);
        return 0;
    }

    status = ares_dns_record_create(&dnsrec2, 0, ARES_OPCODE_QUERY, ARES_RCODE_NOERROR);
    if (status != ARES_SUCCESS) {
        ares_dns_record_destroy(dnsrec1);
        ares_destroy(channel);
        return 0;
    }
    status = ares_dns_record_add_query(dnsrec2, name2, ARES_CLASS_IN, ARES_REC_TYPE_A);
    if (status != ARES_SUCCESS) {
        ares_dns_record_destroy(dnsrec1);
        ares_dns_record_destroy(dnsrec2);
        ares_destroy(channel);
        return 0;
    }

    status = ares_query_dnsrec(channel, &res1, a_callback, dnsrec1);
    if (status != ARES_SUCCESS) {
        ares_dns_record_destroy(dnsrec1);
        ares_dns_record_destroy(dnsrec2);
        ares_destroy(channel);
        return 0;
    }
    // dnsrec1 ownership transferred to c-ares

    status = ares_query_dnsrec(channel, &res2, a_callback, dnsrec2);
    if (status != ARES_SUCCESS) {
        ares_dns_record_destroy(dnsrec2);
        // dnsrec1 already owned by c-ares; we can't free it here
        ares_destroy(channel);
        return 0;
    }
    // dnsrec2 ownership transferred

    // Process events until both callbacks have fired or timeout.
    int max_wait_ms = 5000;
    int waited = 0;
    while (!res1.done || !res2.done) {
        struct timeval tv;
        tv.tv_sec = 0;
        tv.tv_usec = 100000; // 100ms
        ares_process_fd(channel, ARES_SOCKET_BAD, ARES_SOCKET_BAD);
        // Actually we need to wait for events; use ares_process with timeout
        // Better: use ares_wait or ares_process with select-like behavior.
        // For simplicity, we'll call ares_process_fd with both read and write fds.
        // But we need to get fds. Let's use ares_fds and ares_timeout.
        ares_socket_t socks[ARES_GETSOCK_MAXNUM];
        int nfds = ares_getsock(channel, socks, ARES_GETSOCK_MAXNUM);
        fd_set read_fds, write_fds;
        FD_ZERO(&read_fds);
        FD_ZERO(&write_fds);
        int max_fd = -1;
        for (int i = 0; i < nfds; i++) {
            int bit = ares_getsock_readbits(channel, i);
            if (bit) {
                FD_SET(socks[i], &read_fds);
                if ((int)socks[i] > max_fd) max_fd = (int)socks[i];
            }
            bit = ares_getsock_writebits(channel, i);
            if (bit) {
                FD_SET(socks[i], &write_fds);
                if ((int)socks[i] > max_fd) max_fd = (int)socks[i];
            }
        }
        struct timeval *tvp = ares_timeout(channel, NULL, &tv);
        if (tvp == NULL) {
            tv.tv_sec = 0;
            tv.tv_usec = 100000;
            tvp = &tv;
        }
        if (tvp->tv_sec > 5) {
            tvp->tv_sec = 5;
            tvp->tv_usec = 0;
        }
        int sel = select(max_fd + 1, &read_fds, &write_fds, NULL, tvp);
        if (sel < 0) {
            break;
        }
        ares_process_fd(channel,
                        FD_ISSET(ARES_SOCKET_BAD, &read_fds) ? ARES_SOCKET_BAD : (max_fd >= 0 ? (ares_socket_t)max_fd : ARES_SOCKET_BAD),
                        FD_ISSET(ARES_SOCKET_BAD, &write_fds) ? ARES_SOCKET_BAD : (max_fd >= 0 ? (ares_socket_t)max_fd : ARES_SOCKET_BAD));
        // Actually we need to pass the actual fds that are ready. Simplify: pass all fds.
        // Let's just call ares_process_fd with the max fd for both read and write.
        // This is not ideal but works for fuzzing.
        // Better: iterate over socks and call ares_process_fd for each.
        // We'll do a simple approach: call ares_process_fd with the first socket.
        // For robustness, we'll just call ares_process_fd with ARES_SOCKET_BAD for both to process timeouts.
        // But that won't handle I/O. Let's do a proper loop.
        // Actually, let's use ares_process with a single call.
        // We'll just call ares_process_fd with the max fd for both read and write.
        // This is a fuzz driver, so it's acceptable.
        // Let's do it properly:
        for (int i = 0; i < nfds; i++) {
            ares_socket_t s = socks[i];
            int r = FD_ISSET(s, &read_fds) ? 1 : 0;
            int w = FD_ISSET(s, &write_fds) ? 1 : 0;
            if (r || w) {
                ares_process_fd(channel, r ? s : ARES_SOCKET_BAD, w ? s : ARES_SOCKET_BAD);
            }
        }
        // Also process timeouts
        ares_process_fd(channel, ARES_SOCKET_BAD, ARES_SOCKET_BAD);
        waited += 100;
        if (waited > max_wait_ms) break;
    }

    // Consume results
    if (res1.addr) free(res1.addr);
    if (res2.addr) free(res2.addr);

    ares_destroy(channel);
    return 0;
}