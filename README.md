# Novaglide (Ice Hockey Multiplayer Game)

## Overview
This project is a real-time, fast-paced multiplayer game, drawing inspiration from air hockey. Players aim to score more goals than their opponents within a limited time frame. The game introduces unique mechanics like 'hook' and 'dash' spells and currently offers 1v1 matches, with 2v2 matches under development. It features an ELO ranking system and matchmaking. Future enhancements include adding music, improving graphics, and more.

## Features
- **Real-Time Gameplay**: Engage in fast-paced matches against other players.
- **Special Abilities**: Utilize 'hook' and 'dash' spells to outmaneuver opponents.
- **Matchmaking and ELO Ranking**: Compete in matches that fit your skill level.
- **Game Modes**: Play in 1v1 matches, with 2v2 matches coming soon.
- **Future Enhancements**: Planned additions include music, enhanced graphics, and more.

---
## Team Contributions

This game was developed through a collaborative effort between two team members, Tomáš Barhoň & Matěj Schrödl. Below is a breakdown of the primary contributions from each member:

### Tomáš Barhoň's Contributions
- **Networking, Client, and Base Server Development**: Handled the networking aspect of the game, developed the client, and set up the base server, ensuring smooth online interactions.
- **Database Setup**: Led the setup of the game's database and contributed to parts of the database API.
- **Menu Development**: Created several menus including LoginMenu, RankedMenu, LoadingScreenMenu, SettingsMenu, and MatchHistoryMenu.
- **Testing**: Focused on testing various components of the game to ensure functionality and reliability.

### Matěj Schrodl's Contributions
- **Project Concept**: Originated the idea for the game.
- **Core Game Development**: Implemented the main game loop, game entities, and the base menu structure.
- **Database API**: Contributed to the development of parts of the database API.
- **Menu Design**: Developed various menus including EndScreenMenu, Credits, and BaseMenu.
- **Code Quality**: Ensured adherence to PEP8 standards using pylint.


### Collaborative Efforts
In addition to these individual contributions, both M and T worked together on numerous smaller tasks and features, playing a vital role in the overall development and success of the game.

---
## Dependencies
Ensure the following dependencies are installed:
- `pygame==2.5.2`
- `psycopg2-binary==2.9.9`
- `PyYAML==6.0.1`
- `numpy==1.24.4`
- `pytest==7.4.4`
- `pylint==2.4.4`



Install them using:
```
pip install -r requirements.txt

shell
```

## Getting Started
To run the game client:
```
cd src && python3 main.py
```

To start the game server:
```
cd src && python3 server.py
```

## Running Tests
Execute tests from the root directory using:

```
# TODO: tady to doplň Tome
pytest
```

## Docker Support
Docker is used to set up the database required for the server. Start the database with:
```
docker-compose up
```

## Configuration
Adjust game settings in the `/settings` directory:
- `config.yaml`: General configuration settings.
- `settings.json`: Additional settings.
