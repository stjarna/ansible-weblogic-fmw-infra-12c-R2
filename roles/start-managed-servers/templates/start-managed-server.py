connect('{{ weblogic_admin_username }}', '{{ weblogic_admin_pass }}', 't3://{{ admin_ip_public }}:{{ admin_server_port }}')

# start('ms-1')
# start('ms-1','Server','t3://192.168.56.14:8001')

nmConnect('{{ nodemanager_username }}', '{{ nodemanager_password }}', '{{ node_manager_listen_address }}', '{{ node_manager_listen_port }}', '{{ domain_name }}');

nmGenBootStartupProps('ms-1')
nmGenBootStartupProps('ms-2')

# TODO make a loop over managed server names
nmStart('ms-1');
nmStart('ms-2');

# nmDisconnect();