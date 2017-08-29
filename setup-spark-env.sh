# update and upgrade
apt-get update && apt-get upgrade -y

# installing java
apt-get install openjdk-8-jdk openjdk-8-jre -y

# installing scala
wget www.scala-lang.org/files/archive/scala-2.11.7.deb && dpkg -i scala-2.11.7.deb && rm scala-2.11.7.deb

# spark installation
mkdir /working 
cd /working
wget https://d3kbcqa49mib13.cloudfront.net/spark-2.2.0-bin-hadoop2.7.tgz && tar -xzf spark-2.2.0-bin-hadoop2.7.tgz && rm spark-2.2.0-bin-hadoop2.7.tgz && mv spark-2.2.0-bin-hadoop2.7 spark2.2

# setup python environment for python developers
easy_install pip
apt-get install g++ python-dev ipython -y

echo 'SPARK_HOME=/working/spark2.2' >> ~/.bashrc
echo 'export PATH=$PATH:$SPARK_HOME/bin' >> ~/.bashrc

