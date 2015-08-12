# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/precise64"
  
  config.vm.provider "virtualbox" do |vb|
    # Display the VirtualBox GUI when booting the machine
    # vb.gui = true
 
    # Customize the amount of memory on the VM:
    vb.memory = "1024"
  end

  # Salt provisioner
  config.vm.provision :salt do |salt|
    salt.minion_config = 'saltstack/etc/minion/'
    salt.run_highstate = true
    salt.install_type  = "git"
    salt.install_args  = "v2014.1.0"
    salt.verbose       = true
  end

  config.vm.synced_folder "./", "/home/vagrant"
  
end

