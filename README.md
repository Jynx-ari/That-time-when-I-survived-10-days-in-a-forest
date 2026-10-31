# That Time I Got Stranded in a Forest and Had to Defend a Radio Tower for Ten Nights (NOT FINISHED!!)
(learning python again and trying to get gud with AI guiding me)
A 2D top-down pew pew survival and tower defense game made with python and pygame. NOTE: (ITS STILL NOT FINISHED!!)

About the game device support: I actually support Linux more than Windows (since im using Linux right now and my pc cant handle Windows anymore) so I might prefer updating the Linux build more than the windows one (I use wine for building the Windows version)

## Goal:
Survive the nights and protect the radio tower until rescue arrives or smth?


## How to Run

You can play the game using a prebuilt executable or run it from the source code.

### Linux

1. Download the Linux executable from the project's releases.
2. Open a terminal in the directory containing `ForestDefense`.
3. Make the executable runnable and launch it:

   ```bash
   chmod +x ForestDefense
   ./ForestDefense
    ````

### Windows

1. Download `ForestDefense.exe` from the project's releases.
2. Double-click `ForestDefense.exe` to launch the game.

### Running on Linux with Wine

If you want to run the Windows version on Linux, install Wine and run:

```
wine ForestDefense.exe
```

### Running from Source

Make sure Python and Pygame are installed, then run:

```
python -m pip install pygame
python main.py
```

## Controls

### Main Menu
| Key | Action |
|---|---|
| `ENTER` | Start Game |
| `ESC` | Quit Game |

### Gameplay
| Key / Input | Action |
|---|---|
| `W A S D` | Move |
| `Arrow Keys` | Move |
| `Mouse Movement` | Aim |
| `Left Mouse Button` | Shoot |
| `1 – 3` | Select Hotbar Slot |
| `B` | Toggle Backpack |
| `Mouse Wheel` | Zoom In / Out |
| `HOME (the home button thingy on your keyboard)` (3 times quickly) | Quit Game |
### Debug controls (cuz its still not finished :< )
| Key / Input | Action |
|---|---|
| `SPACE` | Start Night Wave | 
| `C` | Clear Active Wave |
| `N` | Advance to Next Day |


### Backpack
| Input | Action |
|---|---|
| `B or ESC (if backpack is open)` | Open / Close Backpack |
| `Left Mouse Button` | Pick Up / Move Items in Inventory | 
| `Left Mouse Button` (Release) | Place / Swap Items in Inventory|

### Developer / Debug
| Feature | Details |
|---|---|
| Path Visualization | Available through `game_conf["debug paths"]` in `main.py`; disabled by default |
| Console Logs | Displays forest generation, obstacle creation, pathfinding time, tower position, and reachable cells |

## Status
WORK IN PROGRESSS RAHH!!!!!

 - (Prep-Week 3 SHIP APPROVED)
 - (Week 1 SHIP APPROVED)
 - (Week 2 SHIPPED! STILL ON VOTING THEN REVIEW!)
 - (Week 3 None)
 - (Week 4 None)
 - And so on...
