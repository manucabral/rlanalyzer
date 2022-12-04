# rlanalyzer
A lightweight Python library for extract Rocket League log information.

It can be used to get information about the current match or player without using BakkesMod or another mod.

This library is not affiliated with Psyonix, Inc.
### Features
- Extract current log information
- Extract another log stored
- Extract player data
- Detects maps, game class, and more
- Detects platform (Epic or Steam)

### Installation
PyPI package is not available yet, clone it.
```bash
git clone https://github.com/manucabral/rlanalyzer.git
```

### Usage
Setting up
```py
from rlanalyzer import Analyzer

analyzer = Analyzer()
```
Let's get some info
```py
print(analyzer.platform)
print(analyzer.version)
print(analyzer.game_running)
print(analyzer.gameclass)
print(analyzer.map)
print(analyzer.freeplay)
print(analyzer.in_party)
```
Get current player
```py
player = analyzer.player
print(player.name, player.platform, player.platform_id)
```
Get current party
```py
party = analyzer.party
print(party.party_id)
print(party.size)
print(party.leader)
print(party.members())
```

### Constributions
All constributions, bug reports or fixes and ideas are welcome.
