Vagrant.configure(2) do |config|
  
  config.vm.box = "centos/7" 
  config.vm.network "private_network", ip: "192.168.56.14"
  config.vm.hostname = "wls12c-r2-1.private"
  config.vm.network "forwarded_port", guest: 22, host: 2022 
  
  config.vm.provider "virtualbox" do |vb|  
    vb.memory = "8192"
    vb.cpus = 4
    vb.name = "Weblogic12cR2-1"
  end
end
