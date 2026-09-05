# LÖVE (Love2D) :material-heart-circle:

[LÖVE](https://love2d.org/) is a lightweight 2D framework for games written in
Lua. It's popular for indie games and prototypes thanks to its simplicity, fast
iteration and cross-platform support.

LÖVE games are among the easiest things to port. The framework is open source
and builds natively for ARM, and the game itself is Lua source plus assets
rather than compiled code, so the same game files usually run unmodified.

LÖVE is one of the more common engines in the library. A handful of those ports
use it only for a launcher front-end rather than for the game itself.

## How PortMaster runs it

There is no compatibility layer here. A LÖVE build for ARM runs the game
directly.

**Use the included `love_11.5` runtime.** This is the preferred method and what
a new port should do. PortMaster ships the LÖVE runtime centrally, so the port
carries only the game itself: no engine binary, no shared libraries, nothing to
rebuild when LÖVE is updated.

The launch script sources the runtime, which sets everything needed:

```bash
# Set the XDG environment variables for config & savefiles
export XDG_DATA_HOME="$CONFDIR"
export SDL_GAMECONTROLLERCONFIG="$sdl_controllerconfig"

# Source love2d runtime
source $controlfolder/runtimes/"love_11.5"/love.txt

# Use the love runtime
$GPTOKEYB "$LOVE_GPTK" &
pm_platform_helper "$LOVE_BINARY"
$LOVE_RUN gamedata

pm_finish
```

Sourcing `love.txt` provides three things:

| Variable | What it is |
|---|---|
| `$LOVE_RUN` | The command that runs the game. Give it the game directory or `.love` file. |
| `$LOVE_BINARY` | Path to the LÖVE executable, for `pm_platform_helper`. |
| `$LOVE_GPTK` | The runtime's default gptokeyb config, so controls work without shipping one. |

`love_11.5` is the only shared LÖVE runtime PortMaster ships, and every port
using the runtime targets it. Target 11.5 unless the game genuinely cannot run
on it.

**Bundling a LÖVE binary in the port** is the older approach. Those ports carry
their own `love` executable and its shared libraries inside the port folder,
which costs size, has to be maintained per port, and misses fixes made to the
shared runtime. Only do this when the game will not run on
11.5 and there is no way around it.

## Compatibility

Most LÖVE games port without modification. The things that cause trouble:

- **LuaJIT FFI and native C libraries.** Anything calling into a compiled `.so`
  needs that library rebuilt for ARM. This is the most common blocker.
- **Shaders.** Handhelds run OpenGL ES, and GLSL written against desktop OpenGL
  may not compile.
- **LÖVE version differences.** The 0.x to 11.x API changes are significant.
  A game written for 0.10 will not run on 11.5 unmodified.
- **Resolution and asset size.** Large textures and heavy per-frame drawing hit
  low-end devices hard.

## Identifying a game

A `.love` file is just a zip archive. Rename or unzip it and the game's source
is right there, which makes LÖVE games unusually easy to inspect before
committing to a port.

- `main.lua` is the entry point and confirms it's a LÖVE game.
- `conf.lua` normally declares the LÖVE version the game targets, via
  `t.version`. This is the value to match against the runtime.

Games can be distributed either as a `.love` archive or as a plain directory
containing `main.lua`. LÖVE runs both, so a port can use whichever the game
shipped.

## Port structure

A port using the shared runtime holds nothing but the game and its config:

```
Curse of the Arrow.sh
curseofthearrow/
├── gamedata/
│   ├── main.lua
│   ├── conf.lua
│   └── assets/
├── conf/
│   └── love/
│       └── CurseOfTheArrow/
├── LICENSE.game.txt
└── LICENSE.love2d.txt
```

**`gamedata/`** is the game itself, either an unpacked directory with `main.lua`
at its root or a single `.love` file.

**`conf/`** is where saves and config go. The launch script points
`XDG_DATA_HOME` at it, so LÖVE writes into the port folder instead of the
user's home directory. LÖVE creates a subdirectory named after the game's
identity, which is why the path has that extra level.

A port that bundles its own binary carries the runtime too. This is the older
layout, shown here for when you have to read one:

```
cityglitch/
├── bin/
│   └── love
├── libs/
│   ├── liblove-11.5.so
│   ├── libluajit-5.1.so.2
│   ├── libmodplug.so.1
│   └── libogg.so.0
└── cityglitch.gptk
```

**`bin/love`** is the LÖVE executable, and **`libs/`** holds the shared
libraries it links against. The launch script adds `libs/` to
`LD_LIBRARY_PATH` before running it.

## Patching and common fixes

Because the game is Lua source, fixes are usually applied by editing the game's
own files at package time or in a `patchscript`, rather than by binary patching.

**Rebuilding native dependencies.** If the game uses FFI to call a C library,
that library has to be compiled for ARM and shipped in the port's `libs/`
folder.

**Rewriting shaders.** GLSL that assumes desktop OpenGL often needs adjusting
for OpenGL ES. Precision qualifiers are a common cause of shader compile
failures.

**Resolution handling.** Games that assume a fixed desktop resolution may need
their `conf.lua` or window setup adjusted for handheld screens.

**Controller input.** Games built for keyboard and mouse are mapped with
gptokeyb via the port's `.gptk` file, the same as any other port.

## Tools

- [LÖVE](https://love2d.org/) is the framework itself, and the desktop build is
  useful for testing changes before putting them on a device.
- Any zip tool will open a `.love` archive, since that's all it is.

## Example ports

Real LÖVE ports in the library, useful to unpack and look at:

Using the shared `love_11.5` runtime, which is what a new port should copy:

- [Balatro](../../../../port/?name=balatro)
- [Curse of the Arrow](../../../../port/?name=curseofthearrow)
- [Gravity Circuit](../../../../port/?name=gravitycircuit)
- [Friday Night Funkin](../../../../port/?name=fridaynightfunkin)

Bundling their own LÖVE binary, the older approach:

- [Blue Revolver](../../../../port/?name=bluerevolver)
- [City Glitch](../../../../port/?name=cityglitch)
