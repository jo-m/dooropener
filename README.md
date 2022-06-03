# Coworking Space Door Opener

This was in use at the old ETH Entrepreneur Club Coworking Space.

The door opener is actuated through a RasPi GPIO pin, which is connected to the building door opener through a relay.

Running on a Raspberry Pi. [Setup](SETUP.md).

## Local setup
    pip install virtualenv
    virtualenv -p python3 .venv
    source .venv/bin/activate
    pip install -r requirements.txt

    # run app
    ./dooropener.py

Die App ist nun hier erreichbar: <http://localhost:5050>.
