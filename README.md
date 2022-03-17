# Troll Bay

## Presentation
Troll Bay is a simple 1 VS 1 dual game. You control a troll and the goal is to beat your opponent !
Our game is playable using the local network of your router
## Installation and Initialisation
When the project is clone into your folder, you will have to install all the packages required for the well running of the game.
```bash
pip3 install
```
All the required packages are listed in the `requirements.txt` so the last command should install them automatically.
If not you have to run this command for every package :
```bash
pip3 install name_of_the_package
```

Then at the root of the project you'll found an `.env.example` file.  
Please copy it by naming it `.env`  
Finally at the line `SERVER_IP=YOUR_IP_ADDRESS` paste you own IP address.
___
## Start
You may are impatient to launch the game by now !
Don't worry after 3 littles bash commands you'll be able to play !

First the server must be launched : 
```bash
python3 server.py
```
If the server has succesfully started, the terminal should have print *Waiting for a connection, Server started*
If not please check your IP address and/or the Port you are using

Then launch in a second a terminal
```bash
python3 client.py
```