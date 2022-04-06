# PvZSurvival
Controls cannon launch and card select by keyboard input to play more conveniently at the six Plants vs. Zombies survival endless levels!

## Dependencies

* Python 3.6 or higher.
* pynput==1.7.6
* pywin32==303
* playsound==1.2.2
  `pip install playsound==1.2.2`

## How to Use

* Run `Main.py` with Python 3.
* Input `Alt + 1~6` to enter the key mode of the six survival levels, namely **Day**, **Night**, **Pool**, **Fog**, **Roof** and **Moon**.
* Press `1` `2` `3` `4` `5` to **launch cannon pairs** to the right side of the screen, or press `Q` `W` `E` `R` `T` to make the point of fall a column lefter than above.
* Press `F2` `F3` `S` `D` or `Enter` to **select cards**.
* Press `H + Alt` to **halt** (back to the main menu so that you can choose a different survival key mode).
* Press `Alt + Q` in main menu to **quit**.

## Scripts

- Main.py - Program entry.
- Survival.py - The base class for different survival levels.
- FrontYard.py - The derived class of `Survival` for **Day** and **Night**.
- BackYard.py - The derived class of `Survival` for **Pool** and **Fog**.
- Roof.py - The derived class of `Survival` for **Roof** and **Moon**.



