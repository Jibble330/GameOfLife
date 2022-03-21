# Conway's Game of Life
Recreation of Conway's Game of Life in Python

Use the middle mouse button to move around, space to start and pause the game, click on tiles to toggle them on or off, and finally **esc** to exit. You can also use the scroll wheel to zoom in and out, and change the speed with the slider in the bottom right. <br/>

---

If the attached exe does not work, or you are not on a windows machine, I would reccomend using Nuitka. This is because Nuitka compiles Python to C, causing it to be detected by much fewer antivirus programs, unlike pyinstaller.<br/><br/>
For *Windows* I used these commands, but you can find the documentation [here](https://nuitka.net/doc/user-manual.html):

```
python -m pip install nuitka

nuitka --onefile --windows-icon-from-ico=GameOfLife.ico --windows-disable-console --enable-plugin=numpy --mingw64 GameOfLife.py
``` 
<br/>

**Optional:** For extra compression, install the *zstandard* library with this command:

```python -m pip install zstandard```

---

**Example of how it plays:**
![Conway's Game of Life](https://user-images.githubusercontent.com/87543311/159214315-5f2e6621-a5a0-4055-861a-a94c7dc36fd0.gif)

---

**Problems:** <br/><br/>
The theoretically infinite grid is only **1000x1000** due to processing constraints and loading times. It may be able to handle sizes above this due to recent optimizations, but it has not been tested.
