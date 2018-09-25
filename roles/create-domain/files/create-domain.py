import time

from java.io import FileInputStream
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

def createTheDomain():
  print 'Creating domain name=[' +var_domain_name +'] in path=[' + var_domain_dir + ']...'
  createDomain(getProperty('weblogic.home.path') + '/common/templates/wls/wls.jar', var_domain_dir, var_adminServer_username, var_adminServer_Password)

  print 'Reading domain in WLST Offline Mode...'
  readDomain(var_domain_dir)

  print 'Setting Domain properties...'
  cd('/')
  cmo.setExalogicOptimizationsEnabled(false)
  cmo.setClusterConstraintsEnabled(false)
  cmo.setGuardianEnabled(false)
  cmo.setAdministrationPortEnabled(false)
  cmo.setConsoleEnabled(true)
  cmo.setConsoleExtensionDirectory('console-ext')
  cmo.setProductionModeEnabled(false)
  cmo.setAdministrationProtocol('t3s')
  cmo.setConfigBackupEnabled(false)
  cmo.setConfigurationAuditType('none')
  cmo.setInternalAppsDeployOnDemandEnabled(false)
  cmo.setConsoleContextPath('console')

  cd('/Servers/AdminServer')
  cmo.setListenPortEnabled(true)
  cmo.setAdministrationPort(int(var_adminServer_admin_port))

  print 'Setting Admin Listen Address to IP=[' + var_adminServer_listen_address + ']'
  cmo.setListenAddress(var_adminServer_listen_address)

  print 'Setting Admin Listen Port to [' + var_adminServer_listen_port + ']'
  cmo.setListenPort(int(var_adminServer_listen_port))

  cmo.setWeblogicPluginEnabled(false)
  cmo.setJavaCompiler('javac')
  cmo.setStartupMode('RUNNING')
  cmo.setVirtualMachineName(var_domain_name+'_AdminServer')
  cmo.setClientCertProxyEnabled(false)

#################

def createMachines():
  print 'Creating ' + str(var_managed_server_count) + ' Machines...'

  for n in range(1, var_managed_server_count+1):

    var_machine_name = 'm' + str(n)
    var_vm_pub_ip = getProperty('vm' + str(n) +'.ip.public')
    var_vm_pri_ip = getProperty('vm' + str(n) +'.ip.private')

    print 'Creating machine name=[' + var_machine_name + ']...'
    cd('/')
    create(var_machine_name, 'Machine')
    cd('/Machines/' + var_machine_name + '/')

    create(var_machine_name, 'NodeManager')
    cd('/Machines/' + var_machine_name + '/NodeManager/' + var_machine_name)

    ## JW: I suggest Plain NodeManager and they can worry about certificates, unless its easy to create and assign them
    set('NMType', 'Plain')

    print 'Setting Listen Address for machine=[' + var_machine_name + '] to IP=[' + var_vm_pri_ip + ']'
    set('ListenAddress', var_vm_pub_ip)
    set('ListenPort', int(var_nodemanager_listen_port))

#################

def createCluster():
  cd('/')
  print 'Creating cluster name=[' + var_cluster_name + ']...'
  create(var_cluster_name, 'Cluster')
  cd('/Clusters/' + var_cluster_name)

  # need to make this option selectable
  # cmo.setMigrationBasis('consensus')

  # need to loop this and create the array
  # set('CandidateMachinesForMigratableServers',jarray.array([ObjectName('com.bea:Name=m1,Type=Machine'), ObjectName('com.bea:Name=m2,Type=Machine')], ObjectName))

#################

def createManagedServers():
  print 'Creating ' + str(var_managed_server_count) + ' Servers...'
  for n in range(1, var_managed_server_count+1):

    var_machine_name = 'm' + str(n)
    var_ms_name = var_ms_name_base + '-' + str(n)
    var_ms_listen_port = int(var_ms_port_base + str(n))
    var_ms_listen_address = getProperty('vm' + str(n) + '.ip.public')
    var_vm_pub_ip = getProperty('vm' + str(n) +'.ip.public')
    var_vm_pri_ip = getProperty('vm' + str(n) +'.ip.private')

    cd('/')
    print 'Creating Server Name=[' + var_ms_name + ']...'
    create(var_ms_name, 'Server')

    cd('/Servers/' + var_ms_name)

    print 'Setting Listen Port=[' + str(var_ms_listen_port) + '] for Managed Server name=[' + var_ms_name + ']...'
    set('ListenPort', int(var_ms_listen_port))

    print 'Setting Listen Address=[' + str(var_ms_listen_address) + '] for Managed Server name=[' + var_ms_name + ']...'
    set('ListenAddress', var_ms_listen_address)

    print 'Setting Machine=[' + var_machine_name + '] for Managed Server name=[' + var_ms_name + '] ...'
    set('Machine', var_machine_name)

    print 'Assigning Server [' + var_ms_name + '] to cluster [' + var_cluster_name + ']...'
    assign('Server', var_ms_name, 'Cluster', var_cluster_name)

#############

#####################################################################################################################
#####################################################################################################################

myProps = loadMyProperties('/oracle/fmw12.2.1/installer/domain.properties')

var_domains_dir = getProperty('user.projects.path') + '/'
var_domain_name = getProperty('domain.name')
var_domain_dir = var_domains_dir + var_domain_name

var_adminServer_username = getProperty('admin.server.username')
var_adminServer_Password = getProperty('admin.server.password')
var_adminServer_listen_address = getProperty('vm-admin.ip.public')
var_adminServer_listen_port = getProperty('admin.server.listen.port')
var_adminServer_admin_port = getProperty('admin.server.administration.port')
var_cluster_name = getProperty('cluster.name')
var_managed_server_count = int(getProperty('managed.server.count'))
var_ms_name_base = getProperty('managed.server.name.base')
var_ms_port_base = getProperty('managed.server.port.base')
var_nodemanager_listen_port = getProperty('nodemanager.listen.port')


createTheDomain()
createMachines()
createCluster()
createManagedServers()

updateDomain()
exit()