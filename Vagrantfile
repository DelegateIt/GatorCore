# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/precise64"
  
  # config.vm.provider "virtualbox" do |vb|
    # Display the VirtualBox GUI when booting the machine
    # vb.gui = true
 
    # Customize the amount of memory on the VM:
    # vb.memory = "1024"
  # end

  config.vm.network "forwarded_port", guest: 8080, host: 8080
  config.vm.network "forwarded_port", guest: 4848, host: 4848
  config.vm.network "forwarded_port", guest: 7676, host: 7676
  config.vm.synced_folder "./", "/home/vagrant"
  config.vm.provision "shell", :path => "bootstrap.sh"
  
end
