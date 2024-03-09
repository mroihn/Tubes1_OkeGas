# Etimo Diamonds Challenge
>Tugas Besar IF2211 Strategi Algortima
## General Information 
This repository contains the implementation of Etimo Diamonds Bot using Greedy Algorithm.
## Technology Used
- node.js
- python 3
## Contributors (OkeGas)
| NIM | Nama |
| :---: | :---: |
| 13522151 | Samy Muhammad Haikal |
| 13522152 | Muhammad Roihan  |
| 13522154 | Chelvadinda |
## Strategy
The bot will use Greedy Algorithm to determine the best strategy
1. Calculate the density of Diamond Game Objects by using point/distance
2. Set the goal position to the diamond with the largest density
3. If Inventory is full go back to base


## Game Engine Setup
1. [Click here to Download And Setup Game Engine](https://github.com/haziqam/tubes1-IF2211-game-engine/releases/tag/v1.1.0) 
2. Make Sure You already installed yarn by using `npm install --global yarn`
3. Go into the root directory `cd tubes1-IF2110-game-engine-1.1.0` and install dependencies using `yarn`
4. Setup environment variables `./scripts/copy-env.bat`
5. Setup local database(make sure docker is already running) `docker compose up -d database`
6. Run this script `./scripts/setup-db-prisma.bat`
7. Build using `npm run build`

## Running the Game
1. Clone this repository
`git clone https://github.com/mroihn/Tubes1_OkeGas.git`
2. Install dependencies `pip install -r requirements.txt`
3. Go into the root directory of game engine `cd tubes1-IF2110-game-engine-1.1.0` and Start the frontend `npm run start`
4. Go back to bot directory `cd Tubes1_OkeGas` and run the bot. You can run it using
```python
python main.py --logic Greedy2 --email=your_email@example.com --name=your_name --password=your_password --team etimo
```
or by modifying the `run-bots.bat` file then executing `./run-bots.bat` for example 
```
start cmd /c "python main.py --logic Greedy2 --email=test1@email.com --name=g2 --password=123456 --team gas"
```

6. Acces the frontend from (http://localhost:8082/)
7. More instructions please head to
[Etimo Diamonds GitHub Repository](https://github.com/Etimo/diamonds)

## Documentation
