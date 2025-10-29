# Retro Platformer (Pyxel)

This project is a small retro-style 2D platformer built with Python and Pyxel.  
It recreates the feel of classic side-scrolling platform games: moving across a level, jumping on platforms, breaking blocks, collecting items, avoiding (or defeating) enemies, managing time, and trying not to lose all your lives.

⚠️ This is a personal / academic exercise.  
⚠️ It is not a commercial product.  
⚠️ I am not trying to profit from or compete with any existing game or brand.

I’m sharing this to show what I built and how it plays — not to create any kind of IP conflict.


---

## Core Gameplay

- **Side-scrolling level**  
  The camera follows the player as you move to the right through the level.

- **Jump / gravity / fall**  
  You can run, jump, land on platforms, and fall if there’s no ground.

- **Breakable and “?” blocks**  
  Some blocks can be hit from below. “?”-style blocks can release items such as:
  - **Coins** (give score and increase coin count)
  - **Mushrooms / power-ups** (temporarily upgrade the player)

- **Power-up state**  
  Picking up certain items powers up the player (bigger form, extra hit safety, bonus score).

- **Enemies**  
  Enemies patrol the ground, turn around when they hit obstacles, and interact with the player:
  - Jumping on top of them defeats them and gives points.
  - Touching them from the side can hurt you or cost a life.

- **Score / coins / timer / world / lives HUD**  
  On screen you see:
  - Current score
  - Coin counter
  - World label (e.g. `1-1`)
  - Remaining time
  - Remaining lives

- **Lives and Game Over**  
  If you take too much damage or run out of lives, the run ends.  
  If you collect power-ups, you can survive hits that would normally knock you out.

- **Timed pressure**  
  There’s a countdown. When time hits zero, you lose the life / run instead of just casually walking forever.


---

## Controls

Default controls (keyboard):

- **← / →** : Move left / right  
- **↑** : Jump  
- **Q** : Quit the game

These are mapped using Pyxel’s built-in key handling.


---

## How to Run the Game

You’ll need:
- Python 3.x (tested with Python 3.13)
- [Pyxel](https://github.com/kitao/pyxel) installed

1. Install Pyxel:
   pip install pyxel

2. Add your own assets

    - Create a folder called `assets/` in the project root.
    - Add a Pyxel resource file (for example: `assets/gameassets.pyxres`) with **your** sprites / tiles / sounds.
    - You can create this file using Pyxel’s built-in editor (pixel art, tilemap, etc.).
    - Make sure the game loads that file using a line like:
      pyxel.load("assets/gameassets.pyxres")

3. Run the game:
    python main.py

---

### Important

- This repository does **not** include any sprites, tilemaps, music, sound effects, logos or other visual/audio assets.  
- You are expected to provide your own original assets, placeholders, or public-domain assets.
- When the window opens, you should see the level, your character, HUD (score / time / lives), and you can start moving and jumping.

---

## Why assets are not included

To avoid any possible legal issue:

- No character sprites, enemy sprites, block sprites, logos, sounds, or music are shipped here.
- The `.pyxres` resource file that normally contains those things is **intentionally not included**.
- The `assets/` folder is also intentionally ignored in version control.

Some visuals and behavior are clearly inspired by famous 8-bit era platformers (for example: walking enemies you can stomp, “?”-style item blocks, mushrooms that power you up, etc.).  
Those ideas are part of classic platformer vocabulary — but the original art, characters, names, and sounds are usually copyrighted/trademarked by companies like Nintendo.

So, to be respectful:

- I do **not** publish any of that art here.
- You must plug in your own art locally if you want to run it.

---

## Legal / Respect for IP

Let's be 100% explicit:

- This is a **learning project**.  
  I built it to practice gameplay mechanics (movement, collisions, items, enemies, HUD, lives, timer) and to understand how a retro platformer works.
- This project is **not affiliated with, endorsed by, or sponsored by Nintendo or any other company**.
- I am **not** selling this. I am **not** trying to pass anyone else’s IP as mine.
- The reference to “classic platformers” or “Super Mario–like behavior” is purely descriptive so people understand what kind of gameplay this is.
- If you are a rights holder and you believe something here is a problem, please open an issue or contact me and I will address it immediately.  
  I do not want trouble.

---

## License

- The logic/implementation in this repository is released under the **MIT License**.
- The license covers the logic itself, **not** any third-party brands or artwork.
- Visual/audio assets are **not** included and are **not** licensed here. You must use your own assets or assets you have the right to use.

See `LICENSE` for full terms.

---

## Summary

- Retro-style 2D platformer.  
- Movement, jump, gravity, enemies, power-ups, breakable blocks.  
- Score, timer, lives, HUD, and game over screen.  
- Runs with Python + Pyxel.  
- You provide the art/sound.  
- Shared for learning and portfolio reasons only, not for commercial use.  

I’m sharing this in good faith and with respect. I do not intend to violate anyone's IP or cause problems.
