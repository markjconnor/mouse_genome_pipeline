output host_ips {
  value = harvester_virtualmachine.host[*].network_interface[0].ip_address
}

output host_ids {
  value = harvester_virtualmachine.host.*.id
}

output host_urls {
  value = harvester_virtualmachine.host.*.tags.condenser_ingress_prometheus_hostname
}

output worker_ips {
  value = harvester_virtualmachine.worker[*].network_interface[0].ip_address
}

output worker_ids {
  value = harvester_virtualmachine.worker.*.id
}

output worker_urls {
  value = harvester_virtualmachine.worker[*].tags.condenser_ingress_node_exporter_hostname
}
