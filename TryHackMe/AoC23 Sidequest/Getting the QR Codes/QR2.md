# QR 2

it's on Day 6 of AoC23.
i know two ways to get this: the intended one with the ghost, and the unintended.

### the intended way
using the buffer overflow, get the item with index 'A' in your inventory, that doesn't exist in the shop. it's a yeti badge.
when talking to the shop keeper, he'll tell you that it's not the true yeti badge. if you have enough money, he will give you the true yeti badge for it. so, get yourself as much money as you can and talk to him.

A ghost should've appeared now. talk to him, and he'll tell you what you have to do. you have to:
- have the true Yeti badge in your inventory
- rename the characters the way the ghost tells you
- have exactly 1337 coins after renaming them
- talk to the shop keeper and the name changer
- use the [Konami Code](https://en.wikipedia.org/wiki/Konami_Code)

Use the buffer overflow for renaming characters. at the end of each name, there should be a hex 00 character. hex 00 will be appended to everything you tell the name changer. if you tell him, to name you 'Snowball', you will actually write 'Snowball'+hex 00. You can use this to put hex 00 everywhere you want.
before naming your cat snowball, you have to give yourself the right amount of money, so that you'll have exactly 1337 coins after typing 'Snowball'


when you have renamed everyone and got 1337 coins, talk to the shop keeper and the name changer again just to be sure. then type the konami code, and something weird should happen.

### the unintended way

right click and click on 'inspect element'. when searching for 'qr' in in index.js, you'll find what position 'qr_map' is stored at in the data file the website loads.
at that position in the data file, you'll find some numbers that probably tell the game how to draw the stuff that you see after going the intended path.
there's a square of 50s and 30s in there. convert it to an image using python or by manually typing pixels in some pixel drawing program. 50 means black, 30 means white.


