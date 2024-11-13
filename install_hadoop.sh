#!/bin/bash

# Variables
HADOOP_VERSION="3.3.1"
HADOOP_URL="https://archive.apache.org/dist/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz"
HADOOP_INSTALL_DIR="/usr/local/hadoop"
HADOOP_USER="hadoop"

# Update system and install dependencies
echo "Updating system and installing Java..."
sudo pacman -Syu --noconfirm
sudo pacman -S --noconfirm jdk-openjdk wget

# Check Java installation
if ! java -version; then
  echo "Java installation failed. Exiting..."
  exit 1
fi

# Create Hadoop user
echo "Creating Hadoop user..."
sudo useradd -m -s /bin/bash $HADOOP_USER
echo "$HADOOP_USER:password" | sudo chpasswd
sudo usermod -aG wheel $HADOOP_USER

# Download and extract Hadoop
echo "Downloading Hadoop..."
wget $HADOOP_URL -P /tmp
echo "Extracting Hadoop..."
sudo tar -xzf /tmp/hadoop-$HADOOP_VERSION.tar.gz -C /usr/local
sudo mv /usr/local/hadoop-$HADOOP_VERSION $HADOOP_INSTALL_DIR
sudo chown -R $HADOOP_USER:$HADOOP_USER $HADOOP_INSTALL_DIR

# Set environment variables for Hadoop
echo "Setting environment variables..."
HADOOP_ENV_VARS="export JAVA_HOME=$(readlink -f /usr/bin/java | sed \"s:/bin/java::\")
export HADOOP_HOME=$HADOOP_INSTALL_DIR
export PATH=\$PATH:\$HADOOP_HOME/bin:\$HADOOP_HOME/sbin
export HADOOP_CONF_DIR=\$HADOOP_HOME/etc/hadoop
"
echo "$HADOOP_ENV_VARS" | sudo tee -a /home/$HADOOP_USER/.bashrc
source /home/$HADOOP_USER/.bashrc

# Configure Hadoop files
echo "Configuring Hadoop core-site.xml..."
cat <<EOL | sudo tee $HADOOP_INSTALL_DIR/etc/hadoop/core-site.xml
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://localhost:9000</value>
    </property>
</configuration>
EOL

echo "Configuring Hadoop hdfs-site.xml..."
cat <<EOL | sudo tee $HADOOP_INSTALL_DIR/etc/hadoop/hdfs-site.xml
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>
    <property>
        <name>dfs.namenode.name.dir</name>
        <value>file:///home/$HADOOP_USER/hadoopdata/hdfs/namenode</value>
    </property>
    <property>
        <name>dfs.datanode.data.dir</name>
        <value>file:///home/$HADOOP_USER/hadoopdata/hdfs/datanode</value>
    </property>
</configuration>
EOL

echo "Configuring Hadoop yarn-site.xml..."
cat <<EOL | sudo tee $HADOOP_INSTALL_DIR/etc/hadoop/yarn-site.xml
<configuration>
    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>
</configuration>
EOL

echo "Configuring Hadoop mapred-site.xml..."
cp $HADOOP_INSTALL_DIR/etc/hadoop/mapred-site.xml.template $HADOOP_INSTALL_DIR/etc/hadoop/mapred-site.xml
cat <<EOL | sudo tee -a $HADOOP_INSTALL_DIR/etc/hadoop/mapred-site.xml
<configuration>
    <property>
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
    </property>
</configuration>
EOL

echo "Configuring JAVA_HOME in hadoop-env.sh..."
echo "export JAVA_HOME=$(readlink -f /usr/bin/java | sed 's:/bin/java::')" | sudo tee -a $HADOOP_INSTALL_DIR/etc/hadoop/hadoop-env.sh

# Format the HDFS
echo "Formatting HDFS..."
sudo -u $HADOOP_USER $HADOOP_INSTALL_DIR/bin/hdfs namenode -format

# Start Hadoop services
echo "Starting Hadoop services..."
sudo -u $HADOOP_USER $HADOOP_INSTALL_DIR/sbin/start-dfs.sh
sudo -u $HADOOP_USER $HADOOP_INSTALL_DIR/sbin/start-yarn.sh

echo "Hadoop installation and configuration completed."

# Display service status
echo "Checking Hadoop processes..."
sudo -u $HADOOP_USER jps

echo "Hadoop setup complete. Access the HDFS web interface at http://localhost:9870/ and YARN at http://localhost:8088/"
