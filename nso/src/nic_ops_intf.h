#ifndef __NIC_OPS_INTF_H__
#define __NIC_OPS_INTF_H__

#include "packet.h"

struct nic_info_s {
    int mtu;
    //TODO: add more 
};

typedef struct nic_info_s nic_info_t;

typedef void nic_handle_t;

struct nic_ops_s {
    int (*open)(char *name, nic_handle_t *handle);
    int (*close)(nic_handle_t *handle);
    int (*send)(nic_handle_t *handle, packet_t *p);
    int (*receive)(nic_handle_t *handle, packet_t *p);
    int (*get_info)(nic_handle_t *handle, nic_info_t *info);
};

typedef struct nic_ops_s nic_ops_t;

#endif
