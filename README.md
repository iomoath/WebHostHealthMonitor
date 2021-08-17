Simple script to monitor web host availability

### Features
```
[X] Send alerts via Email
[X] Push alerts to a Slack channel
[X] Monitor multiple hosts
```

### Installation
```
$ cd /opt
$ git clone https://github.com/iomoath/WebHostHealthMonitor.git
$ cd WebHostHealthMonitor
$ pip install -r requirements.txt
```

### Configuration
1. Add URLs would you like to monitor in hosts.json
2. Adjust your settings in config.py

3. Create a cron to run every one minute

```
$ crontab -e

Append the following:

* * * * * /usr/bin/python3 /opt/WebHostHealthMonitor/main.py -c &> /dev/null
```

