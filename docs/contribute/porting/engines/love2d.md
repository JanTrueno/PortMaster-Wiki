# LÖVE (Love2D) :material-heart-circle:

[LÖVE](https://love2d.org/) is a lightweight 2D game framework that uses Lua. It’s widely used for indie games and prototypes thanks to its simplicity, fast iteration, and full cross-platform support.

Porting LÖVE games to ARM-based Linux handhelds is straightforward because LÖVE is open source and compiles natively for ARM. Most games can run unmodified or with minor tweaks.

---

## Porting Methodology

PortMaster runs `.love` files using the system-installed `love` binary or a bundled one. Games can be packaged as:

- A `.love` file
- A directory with `main.lua`

For best compatibility, target **LÖVE 11.5**.

---

## File Structure

---

## Notes

- Games using FFI or native C libraries may require recompilation.
- For best results, avoid using large texture files or heavy shaders on low-end devices.

---

## Tools

- [LÖVE](https://love2d.org/)

---

## Example Games


