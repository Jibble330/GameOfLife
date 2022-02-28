# Conway's Game of Life
Recreation of Conway's Game of Life in Python

Use arrow keys to shift your view, space to start and pause the game, click on tiles to switch them on or off, and finally **esc** to exit. You can also use the scroll wheel to zoom in and out, and change the speed with the slider in the bottom right. <br/>

---

If you would like an exe, I would reccomend using Nuitka. This is because Nuitka compiles python to C, causing it to be detected by much fewer antivirus programs, unlike pyinstaller.<br />
For *Windows* I used these commands:

```
python -m pip install nuitka

nuitka --onefile --windows-icon-from-ico=GameOfLife.ico --windows-disable-console --enable-plugin=numpy --mingw64 GameOfLife.py
``` 
<br/>

**Optional:** For extra compression, install the *zstandard* library with this command:

```python -m pip install zstandard```

---

**Example of how it plays:**
![Conway's Game of Life 2022-02-25 22-40-19](https://user-images.githubusercontent.com/87543311/155833027-6cde3fe1-1000-4236-8e3f-f1bc2f259941.gif)

---

**Problems:** <br/><br/>
The theoretically infinite grid is only **1000x1000** due to processing constraints and loading times. It may be able to handle sizes above this due to recent optimizations, but it has not been tested.
