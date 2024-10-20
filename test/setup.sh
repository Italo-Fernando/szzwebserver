# 
if ! command -v java 2>&1 >/dev/null
then
    echo "java is uninstalled"
    apt-get update
    apt-get install openjdk-11-jdk-headless
fi

if ! command -v /opt/apache-jmeter-5.6.3/bin/jmeter.sh 2>&1 >/dev/null
then
    wget https://dlcdn.apache.org//jmeter/binaries/apache-jmeter-5.6.3.tgz
    tar -xvzf apache-jmeter-5.6.3.tgz
    mv apache-jmeter-5.6.3/ /opt/
    ln -s /opt/apache-jmeter-5.6.3/bin/jmeter.sh /usr/local/bin/jmeter
    rm apache-jmeter-5.6.3.tgz
fi
