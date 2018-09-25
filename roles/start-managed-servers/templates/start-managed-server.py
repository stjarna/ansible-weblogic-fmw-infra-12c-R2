from java.util import Properties

#################

def loadMyProperties(fileName):
    properties = Properties()
    input = FileInputStream(fileName)
    properties.load(input)
    input.close()
    result= {}
    for entry in properties.entrySet(): result[entry.key] = entry.value
    return result

#################

def getProperty(propName):
    return myProps[propName]
#################

#####################################################################################################################
#####################################################################################################################

connect('{{ weblogic_admin_username }}', '{{ weblogic_admin_pass }}', 't3://{{ admin_ip_public }}:{{ admin_server_port }}')

nmConnect('{{ nodemanager_username }}', '{{ nodemanager_password }}', '{{ node_manager_listen_address }}', '{{ node_manager_listen_port }}', '{{ domain_name }}');

myProps = loadMyProperties('/oracle/fmw12.2.1/installer/domain.properties')
var_managed_server_count = int(getProperty('managed.server.count'))

for n in range(1, var_managed_server_count + 1):    
    var_managed_server_name = 'ms-' + str(n)
    print 'Generating startup properties for managed server = [' + var_managed_server_name + ']...'
    nmGenBootStartupProps(var_managed_server_name)
    nmStart(var_managed_server_name);

nmDisconnect();