# Conway's Game of Life
Recreation of Conway's Game of Life in Python

Use arrow keys to move your view, space to start and pause the game, and click on tiles to switch them on or off. <br/>

---

If you would like an exe, I would reccomend using Nuitka. This is because Nuitka compiles python to C, causing it to be detected by much fewer antivirus programs, unlike pyinstaller.<br />
For *Windows* I used these commands:

```
python -m pip install nuitka

nuitka --onefile --windows-icon-from-ico=game-of-life.ico --windows-disable-console --mingw64 GameOfLife.py
```

---

**Example of how it plays:**
![Conway's Game of Life 2022-02-25 22-40-19](https://user-images.githubusercontent.com/87543311/155833027-6cde3fe1-1000-4236-8e3f-f1bc2f259941.gif)

---

**Problems:** <br/>
The theoretically infinite grid in this is only 200x200 due to processing constraints. This is because the algorithim that advances tiles to the next generation checks through *every single* tile in the plane, and every time it checks one tile, it also checks the surrounding 8 tiles, which means it checks about 360,000 tiles multiple times per second. This is obviously not ideal, and there will probably be optimizations in the future, such as only checking tiles surrounding living tiles, which could save lots of processing power, but may still struggle with big patterns. As of now if a tile reaches the edge it simply loops back around, which shouldn't affect small patterns too much.
