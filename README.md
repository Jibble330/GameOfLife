# Conway's Game of Life
Recreation of Conway's Game of Life in python

Use arrow keys to move around, and space to start and pause the game.

---

If you would like an exe, I would reccomend using Nuitka. This is because Nuitka compiles python to C, causing it to be detected by much fewer antivirus programs, unlike pyinstaller.<br />
For *Windows* I used these commands:

```
python -m pip install nuitka

nuitka --onefile --windows-icon-from-ico=game-of-life.ico --windows-disable-console --mingw64 GameOfLife.py
```
