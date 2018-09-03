#ifndef __NSO_H__
#define __NSO_H__

#include "arp.h"
#include "fwding.h"
#include "nso_if.h"
#include "neighbor.h"
#include "nso_common.h"
#include <pthread.h>

#define NSO_MAX_SUPPORTED_IFACES 10
#define NSO_DEFAULT_AGING_PERIOD_MS 2000
#define NSO_DEFAULT_TIMEOUT_MS NSO_DEFAULT_AGING_PERIOD_MS
#define NSO_DEFAULT_SON_REPORT_PERIOD_MS 1000

typedef enum {
    NRG5_UNREG = 0,
    NRG5_REG = 1,
    NRG5_CONNECTED = 2,
}device_status_e;

typedef struct {
    //interface list
    nso_if_t *ifaces[NSO_MAX_SUPPORTED_IFACES];
    int ifaces_nb;

    //arp table
    arp_table_t *arpt;

    //fwding table
    fwd_table_t *son_fwdt;
    fwd_table_t *local_fwdt;

    //neighbor table
    nbr_table_t *nbrt;

    //gw device id
    device_id_t *gw_id;

    //device status
    device_status_e dev_state;
    pthread_mutex_t state_lock;
    pthread_cond_t state_signal;

    //self id
    device_id_t *dev_id;

    //thread handle
    //rx thread: for receiving packets from ifaces
    pthread_t rx_pid;
    //tx thread: for sending control plane packets to xMEC
    pthread_t tx_pid;
    //aging thread: for aging tables
    pthread_t aging_pid;

    int timeout_ms;
    int aging_period_ms;
    //son report period
    int sr_period_ms;
    //it is the maximum among MTUs of interfaces.
    //it is the L2 MTU. That is the length of nso header is inclusive
    int mtu;

} nso_layer_t;


extern nso_layer_t nso_layer;

int nso_layer_run(char *config_file);
int nso_layer_stop();

#endif
