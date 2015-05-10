# Add Required Repositories
sudo add-apt-repository ppa:webupd8team/java -y
sudo apt-get update -yq

# Install OracleJDK & Java Runtime
sudo apt-get install python-software-properties -yq
echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | /usr/bin/debconf-set-selections
sudo apt-get install oracle-java8-installer -yq

# Install Oracle Glassfish
sudo apt-get install unzip
wget --quiet http://download.java.net/glassfish/4.0/release/glassfish-4.0.zip
sudo unzip -q glassfish-4.0.zip -d /opt
rm glassfish-4.0.zip

# Other
sudo apt-get install git
sudo apt-get install xubuntu-desktop
