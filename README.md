# rlanalyzer
A lightweight Python library for extract Rocket League log information.

It can be used to get information about the current match or player without using BakkesMod or another mod.

This library is not affiliated with Psyonix, Inc.
### Features
- Extract current log information
- Extract another log stored
- Detects maps, game class, and more
- Gets player data
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
Get some information
```py
print(analyzer.game)
print(analyzer.map)
print(analyzer.running)
print(analyzer.freeplay)
```
Get current player
```py
player = analyzer.player
print(player.name, player.platform, player.platform_id)
```

### Constributions
All constributions, bug reports or fixes and ideas are welcome.
