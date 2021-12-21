# Copyright 2021 VMware, Inc.
# SPDX-License-Identifier: Apache-2.0

from saltext.vmware.modules import datastore
import saltext.vmware.utils.esxi as utils_esxi


def test_get_datastore(service_instance):
    ret = datastore.get(
        service_instance=service_instance,
        datacenter_name="Datacenter",
        cluster_name="Cluster",
    )
    assert len(ret) >= 1

    hosts = [h.name for h in utils_esxi.get_hosts(get_all_hosts=True, service_instance=service_instance)]
    assert len(ret) == len(hosts)

    for host in hosts:
        assert host in ret
        for ds in ret[host]:
            assert isinstance(ret[host][ds]['total_bytes'], int)
            assert isinstance(ret[host][ds]['free_bytes'], int)
            assert ret[host][ds]['total_bytes'] > ret[host][ds]['free_bytes']

    if len(ret) > 1:
        ret = datastore.get(
            service_instance=service_instance,
            datacenter_name="Datacenter",
            cluster_name="Cluster",
            host_name=hosts[0]
        )
        assert len(ret) == 1
        assert 'total_bytes' in ret[hosts[0]]
