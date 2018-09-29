# ansible-weblogic-fmw-infra-12c-R2
This playbook provides an automated way of Weblogic 12c R2 installation.

Apart environment preparation and installation itself, it also addresses setup of nodemanager and eventual start of admin server and two managed nodes.

The playbook was introduced as a fork of [cvezalis/ansible-weblogic-fmw-infra-12c-R2](https://github.com/cvezalis/ansible-weblogic-fmw-infra-12c-R2) project. Nonetheless an additional refactoring took place. Dependency on Oracle database was also removed since there was no need of Enterprise Manager.

Initial version of WLST script to create a domain was obtained at [oracle/weblogic-innovation-seminars](https://github.com/oracle/weblogic-innovation-seminars/tree/master/WInS_Labs/setup-packages/wlst/starter-cluster).

## Prerequisities
* **Files - host, ansible.cfg**
    * You will likely run the playbook against different host than a VM created by Vagrant. In such case, amend both files accordingly (username, public key, hostname).
* **JDK** 
    * The project does not contain tarball. You have to download JDK 8 b181 at Oracle site
    * Once obtained, please copy it to *roles/install-jdk/files* as *jdk-8u181-linux-x64.tar.gz*
* **WLS installer**
  * The project does not contain installation jar file. You have to download Weblogic installer for WLS12 R2 at Oracle site
    * Once obtained, please copy it to *roles/prepare-wls-env/files* as *fmw_12.2.1.1.0_infrastructure.jar*

## Roles
In order to have all the steps summed up in more organized way, all the steps got split into roles.

Each role deals with particular responsibility.

At the moment, playbook contains following roles:
* **prepare-wls-env**
    * This role tweaks OS, prepares directory structure for the Weblogic installation. Next to directories creation, it also copies installation related files (installer, oraInst etc). 
    * Please note that you have to download real WLS installer from Oracle site.
* **install-jdk**
    * This role handles JDK installation. 
    * Please note that you have to download real JDK tarball from Oracle site.
* **install-wls**
    * This role just executes the installer.
* **create-domain**
    * This roles creates a domain via Wblogic scripting tool (WLST). It creates a cluster of two managed nodes. 
    * It can be easily modified to reduce or increase the number of managed nodes (see more [here](#infra-vars.yml)).
* **setup-node-manager**   
    * This role configures and starts the Nodemanager. 
    * It also configures systemd to start automatically the nodemanager after restart.
* **start-admin-server**
    * This role starts the Admin server using nodemanager.
    * It also contains a wait that block Ansible execution till the Admin server goes up or it may eventually timeout.
* **start-managed-servers**
    * This role starts the two managed nodes using nodemanager.
    * It also contains a wait that block Ansible execution till both managed nodes go up or it may eventually timeout.

## Customization
There are two YML files that enable us to tweak various bits
### infra-vars.yml
This files contains infra related variables. It covers things such as OS Oracle username/password, paths, IP addresses and ports.

If you need to change IP addresses/ports of node manager, admin server or managed nodes, this file is the right place.

If you need to reduce/increase the number of managed nodes, you have to remove vmN_ip_(public|private) properties.  

### wls-vars.yml
This files aims at Weblogic username/password, wls/domain/app related folders.

## Vagrant
You can run this project contains also against VM prepared by Vagrant that is included.

### Steps
* Create environment
    * ``$ vagrant up``
* Destroy environment
    * ``$ vagrant destroy``
* Connect to environment
    * ``$ vagrant ssh``

Vagrant configuration creates a Centos/7 VM with IP address 192.168.56.14.

Please note that the Vagrant does not start deliberatelly Ansible playbook.

Though, once you create VM, you can execute the playbook manually.
``$ ansible-playbook weblogic-fmw-domain.yml``

Once playbook execution completes successfully, you can access Weblogic admin console at http://192.168.56.14:7001/console using following credentials:
* **user** *weblogic*
* **password** *welcome1*