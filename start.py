import subprocess
import os

# Function to run system commands
def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    else:
        print(result.stdout)

# Function to install Java
def install_java():
    run_command("sudo apt update")
    run_command("sudo apt install default-jdk default-jre -y")

# Function to create Hadoop user and configure SSH
def configure_hadoop_user():
    run_command("sudo adduser hadoop")
    run_command("sudo usermod -aG sudo hadoop")
    run_command("sudo su - hadoop")
    run_command("ssh-keygen -t rsa -f ~/.ssh/id_rsa -P ''")
    run_command("cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys")
    run_command("chmod 640 ~/.ssh/authorized_keys")
    run_command("exit")

# Function to install OpenSSH
def install_openssh():
    run_command("sudo apt install openssh-server openssh-client -y")

# Function to download and install Hadoop
def install_hadoop():
    HADOOP_DOWNLOAD_URL = "https://archive.apache.org/dist/hadoop/common/hadoop-3.1.0/hadoop-3.1.0.tar.gz"
    run_command(f"wget {HADOOP_DOWNLOAD_URL} -O hadoop-3.1.0.tar.gz")
    run_command("tar -xzvf hadoop-3.1.0.tar.gz")
    run_command("sudo mv hadoop-3.1.0 /usr/local/hadoop")
    run_command("sudo mkdir /usr/local/hadoop/logs")
    run_command("sudo chown -R hadoop:hadoop /usr/local/hadoop")
    
    hadoop_env_setup = '''
export HADOOP_HOME=/usr/local/hadoop
export HADOOP_INSTALL=$HADOOP_HOME
export HADOOP_MAPRED_HOME=$HADOOP_HOME
export HADOOP_COMMON_HOME=$HADOOP_HOME
export HADOOP_HDFS_HOME=$HADOOP_HOME
export YARN_HOME=$HADOOP_HOME
export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
export PATH=$PATH:$HADOOP_HOME/sbin:$HADOOP_HOME/bin
export HADOOP_OPTS="-Djava.library.path=$HADOOP_HOME/lib/native"
    '''
    
    with open(os.path.expanduser("~/.bashrc"), 'a') as bashrc:
        bashrc.write(hadoop_env_setup)
    
    run_command("source ~/.bashrc")
    
    java_home_command = "$(readlink -f /usr/bin/javac | sed 's:/bin/javac::')"
    hadoop_env_file = "/usr/local/hadoop/etc/hadoop/hadoop-env.sh"
    with open(hadoop_env_file, 'a') as hadoop_env:
        hadoop_env.write(f"export JAVA_HOME={java_home_command}\n")
        hadoop_env.write('export HADOOP_CLASSPATH+=" $HADOOP_HOME/lib/*.jar"\n')

    run_command("cd /usr/local/hadoop/lib")
    run_command("sudo wget https://jcenter.bintray.com/javax/activation/javax.activation-api/1.2.0/javax.activation-api-1.2.0.jar")

# Function to configure core-site.xml
def configure_core_site(dns):
    core_site_content = f"""
<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://{dns}:9000</value>
    </property>
</configuration>
    """
    with open("/usr/local/hadoop/etc/hadoop/core-site.xml", 'w') as core_site_file:
        core_site_file.write(core_site_content)

# Function to configure hdfs-site.xml
def configure_hdfs_site():
    hdfs_site_content = """
<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>
    <property>
        <name>dfs.namenode.name.dir</name>
        <value>file:///home/hadoop/hadoop/hadoopdata/hdfs/namenode</value>
    </property>
    <property>
        <name>dfs.datanode.data.dir</name>
        <value>file:///home/hadoop/hadoop/hadoopdata/hdfs/datanode</value>
    </property>
</configuration>
    """
    with open("/usr/local/hadoop/etc/hadoop/hdfs-site.xml", 'w') as hdfs_site_file:
        hdfs_site_file.write(hdfs_site_content)

# Function to configure yarn-site.xml
def configure_yarn_site(dns):
    yarn_site_content = f"""
<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>
    <property>
        <name>yarn.nodemanager.auxservices.mapreduce.shuffle.class</name>
        <value>org.apache.hadoop.mapred.ShuffleHandler</value>
    </property>
    <property>
        <name>yarn.resourcemanager.hostname</name>
        <value>{dns}</value>
    </property>
</configuration>
    """
    with open("/usr/local/hadoop/etc/hadoop/yarn-site.xml", 'w') as yarn_site_file:
        yarn_site_file.write(yarn_site_content)

# Function to configure Hadoop files
def configure_hadoop_files():
    dns = input("Enter Public DNS/IP or 'localhost' for Hadoop configuration: ")

    # Configure core-site.xml
    configure_core_site(dns)

    # Create HDFS data directories
    run_command("sudo mkdir -p /home/hadoop/hadoop/hadoopdata/hdfs/{namenode,datanode}")
    run_command("sudo chown -R hadoop:hadoop /home/hadoop/hadoop/hadoopdata/hdfs")

    # Configure hdfs-site.xml
    configure_hdfs_site()

    # Configure yarn-site.xml
    configure_yarn_site(dns)

    run_command("hdfs namenode -format")

# Function to start Hadoop services
def start_hadoop_services():
    run_command("start-dfs.sh")
    run_command("start-yarn.sh")

# Function to verify running components
def verify_components():
    run_command("jps")

# Main menu
def main_menu():
    while True:
        print("\nEasyHadoop: Apache Hadoop Installation and Configuration Menu")
        print("1. Install Java")
        print("2. Configure Hadoop User and SSH")
        print("3. Install OpenSSH")
        print("4. Install Hadoop")
        print("5. Configure Hadoop Files")
        print("6. Start Hadoop Services")
        print("7. Verify Running Components")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            install_java()
        elif choice == '2':
            configure_hadoop_user()
        elif choice == '3':
            install_openssh()
        elif choice == '4':
            install_hadoop()
        elif choice == '5':
            configure_hadoop_files()
        elif choice == '6':
            start_hadoop_services()
        elif choice == '7':
            verify_components()
        elif choice == '8':
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main_menu()
