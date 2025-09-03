# WELCOME TO NNS

NNS is a system designed to handle notifications for my home lab server NoxDrive.

The system will work very closly with my API service Nox_API.

Nox

### Running the code.
source ./venv/bin/activate
uvicorn main:app --host 192.168.2.205 --port 2000 --reload
/home/nox/Desktop/NewProjects/NES/venv/bin/python -m uvicorn nns.app.main:app --host 192.168.2.205 --port 2000 --reload