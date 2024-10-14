
# HadoopWizard

![Hadoop](https://img.shields.io/badge/Apache-Hadoop-orange) ![Python](https://img.shields.io/badge/Python-3.x-blue) ![Bash](https://img.shields.io/badge/Shell-Bash-lightgrey)

HadoopWizard is an automation tool designed to simplify the installation and configuration of Apache Hadoop on Linux systems. It streamlines the setup process by handling Java, SSH, and Hadoop installation, as well as configuring core Hadoop files.

## Features

- Install Java (JDK and JRE) required for Hadoop
- Create and configure a dedicated Hadoop user
- Install and configure OpenSSH for Hadoop's secure communication
- Download, install, and configure Hadoop (v3.1.0)
- Configure core Hadoop configuration files (`core-site.xml`, `hdfs-site.xml`, `yarn-site.xml`)
- Format HDFS Namenode and start Hadoop services
- Verify the status of running Hadoop components (via `jps`)

## Prerequisites

Before running HadoopWizard, ensure that your system meets the following requirements:

- **Operating System**: Linux (tested on Ubuntu/Kali)
- **Python**: Version 3.x
- **Bash Shell**
- **Sudo Access**

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/KIRAN-KUMAR-K3/HadoopWizard.git
cd HadoopWizard
```

### 2. Make the Script Executable

Ensure the script has execution permissions:

```bash
chmod +x start.sh
```

### 3. Run the Script

To start the HadoopWizard:

```bash
./start.sh
```

You will be guided through the setup menu to install and configure Hadoop.

### 4. Python Version (Alternative)

If you prefer the Python version of the setup, you can execute the `start.py` file:

```bash
python3 start.py
```

## Menu Options

HadoopWizard offers a simple menu to guide you through various stages of the installation:

1. **Install Java** - Installs the necessary JDK and JRE.
2. **Configure Hadoop User and SSH** - Creates a Hadoop user and sets up SSH keys.
3. **Install OpenSSH** - Installs the OpenSSH server and client for secure communications.
4. **Install Hadoop** - Downloads and installs Hadoop (version 3.1.0).
5. **Configure Hadoop Files** - Configures core Hadoop files like `core-site.xml`, `hdfs-site.xml`, and `yarn-site.xml`.
6. **Start Hadoop Services** - Starts Hadoop services including HDFS and YARN.
7. **Verify Running Components** - Lists running Java processes to confirm Hadoop components are active.

## Troubleshooting

- **Permission Denied Error**: Ensure that the script has execution rights with `chmod +x *`.
- **Python Error**: Ensure that you have Python 3.x installed. Use `python3 --version` to verify.
- **SSH Configuration Issues**: Make sure OpenSSH is correctly installed and the `ssh-keygen` command generates the keys without errors.

## Future Improvements

- Support for Hadoop versions other than 3.1.0.
- Integration of Spark for enhanced data processing.
- Additional configuration options for advanced Hadoop users.

## Contributing

Contributions are welcome! If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcomed.

## License

This project is licensed under the Apache License 2.0. See the `LICENSE` file for more details.

