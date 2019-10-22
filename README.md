# Project Setup

- Install virtualenv_wrapper
- $ mkvirtualenv -p /usr/bin/python3 canphone
- $ workon canphone
- $ pip install -r requirements.txt
- $ pip install -r requirements-dev.txt

# Required packages
```
apt install baresip
apt install mosquitto 

```

# Eventphone extension
- Create account at eventphone.de
- Create extension there

# Configuration
- Copy baresipconf folder to ~/.baresip
- Alter files accounts to match your extension credentials
- Adjust contacts file to match other canphone

# SystemD services
- Copy and enable service files under systemd_service_files
