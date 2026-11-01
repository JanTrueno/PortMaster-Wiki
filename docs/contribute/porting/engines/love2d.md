# LÖVE (Love2D) :material-heart-circle:

[LÖVE](https://love2d.org/) is a lightweight 2D framework for games written in
Lua. It's popular for indie games and prototypes thanks to its simplicity, fast
iteration and cross-platform support.

LÖVE games are among the easiest things to port. The framework is open source
and builds natively for ARM, and the game itself is Lua source plus assets
rather than compiled code, so the same game files usually run unmodified.

LÖVE is one of the most common engines in the library. More than fifty ports use
the shared runtime and more than thirty older ones carry their own copy. A handful
use it only as a launcher front-end for a different engine. PortMaster itself
uses it too, for the patcher screen shown while a port prepares a game on first
launch.

## How PortMaster runs it

There is no compatibility layer. A LÖVE build for ARM runs the game directly.

**Use the `love_11.5` runtime.** PortMaster ships it inside its own folder, so a
port carries only the game: no engine binary, no shared libraries, nothing to
rebuild when LÖVE is updated. It isn't a separately downloaded runtime, so
`runtime` stays empty in `port.json`.

The launch script sources it:

```bash
source $controlfolder/runtimes/"love_11.5"/love.txt
```

That sets the variables a port needs:

| Variable | What it is |
|---|---|
| `$LOVE_RUN` | The command that runs a game. Give it a game directory or a `.love` file. It puts the runtime's own libraries on `LD_LIBRARY_PATH` first, and keeps whatever the port already set. |
| `$LOVE_BINARY` | Path to the LÖVE executable, for `pm_platform_helper`. |
| `$LOVE_GPTK` | The process name gptokeyb watches, `love.aarch64` or `love.x86_64`. Despite the name it is not a config file. See [Input and controls](#input-and-controls). |

`LOVE_VERSION` and `RUNTIME_DIR` are exported as well, though ports rarely need
them.

**Architectures.** The runtime has aarch64 and x86_64 builds, so those are the
two to list in `arch`. armhf is being phased out now that every supported CFW
runs 64-bit, and the runtime has no armhf build.

**Don't bundle LÖVE in a new port.** About thirty older ports carry their own
`love` binary and libraries. That costs size, has to be maintained per port, and
misses fixes made to the shared runtime. They're covered
[at the end](#ports-that-bundle-their-own-love-legacy) so you can read one, not
so you can copy it.

## Identifying a game

LÖVE games ship in three shapes, and all three are zip archives or directories
you can open before committing to a port:

- **A directory** with `main.lua` at its root.
- **A `.love` file.** It is a zip archive, so any zip tool opens it. `main.lua`
  has to sit at the top level of the archive, not inside a folder. A `.love`
  made by zipping a folder will not run.
- **A fused executable.** Windows builds from itch.io, Steam, GOG and Epic are
  usually this: LÖVE's own `.exe` with the game's `.love` archive appended, so
  the one file is both a program and a zip. `unzip` or 7-Zip open it and the
  game's files are inside. MacOS builds hold a plain `.love` inside the app
  bundle, at `Game.app/Contents/Resources`.

`conf.lua`, when present, normally declares the LÖVE version the game targets
through `t.version`. That is the value to compare against the runtime's 11.5.

## Porting a free game, step by step

This is the shape every ready-to-run LÖVE port has. Games the user has to supply
need a few extra steps, covered [below](#games-the-user-supplies).

### 1. Get the game into a shape LÖVE can run

Either unpack it to a directory with `main.lua` at the root, or keep it as a
single `.love`. Check where `main.lua` ended up. If unzipping gives you a single
folder holding everything, the game is that inner folder.

### 2. Lay out the port

```
Curse of the Arrow.sh
curseofthearrow/
├── gamedata/
│   ├── main.lua
│   ├── conf.lua
│   └── assets/
├── conf/
└── licenses/
    ├── LICENSE.game.txt
    └── LICENSE.love2d.txt
```

**`gamedata/`** is the game itself. The name is a convention, not a requirement.
Real ports keep the game in `gamedata/`, `game/`, or as a `.love` file sitting
in the port folder. Whatever you pick, `$LOVE_RUN` is pointed at it.

**`conf/`** is where saves go. See the script below for how it gets used.

**`licenses/`** holds one `LICENSE.<component>.txt` per component, including the
LÖVE license, since the runtime is part of what you're distributing. The
[packaging guide](../packaging.md) covers the rules.

### 3. Write the launch script

Start from the Love2d tab in the [script templates](../script-templates.md). The
header that finds `controlfolder` is the same for every engine. The LÖVE part is
short:

```bash
GAMEDIR=/$directory/ports/curseofthearrow
CONFDIR="$GAMEDIR/conf/"

mkdir -p "$CONFDIR"
cd $GAMEDIR

> "$GAMEDIR/log.txt" && exec > >(tee "$GAMEDIR/log.txt") 2>&1

# Set the XDG environment variables for config & savefiles
export XDG_DATA_HOME="$CONFDIR"
export SDL_GAMECONTROLLERCONFIG="$sdl_controllerconfig"

source $controlfolder/runtimes/"love_11.5"/love.txt

$GPTOKEYB "$LOVE_GPTK" &
pm_platform_helper "$LOVE_BINARY"
$LOVE_RUN gamedata

pm_finish
```

What each part does:

- **`XDG_DATA_HOME`** is where LÖVE writes saves. On Linux it uses
  `$XDG_DATA_HOME/love/<identity>`, so pointing it at `conf/` keeps saves inside
  the port folder, in `conf/love/<identity>`. The identity is the game's
  `t.identity` in `conf.lua`, or whatever it passes to
  `love.filesystem.setIdentity`. Some games write elsewhere and ignore the XDG
  path. For those, the template shows `bind_directories` redirecting the
  location into the port folder.
- **`SDL_GAMECONTROLLERCONFIG`** is the device's controller mapping. LÖVE reads
  gamepads through SDL, so this is what makes the buttons line up.
- **`$GPTOKEYB "$LOVE_GPTK" &`** starts gptokeyb in the background, before the
  game.
- **`pm_platform_helper "$LOVE_BINARY"`** tells the CFW which process is the
  game. muOS records it as the foreground process, and ROCKNIX uses it to
  fullscreen the window under sway.
- **`$LOVE_RUN gamedata`** runs the game. It takes a directory or a `.love`
  file, and ports use both.
- **`pm_finish`** stops gptokeyb and restores the console. Don't hand-roll
  cleanup with `trap` or `pkill`.

Use LF line endings in the `.sh` and any `.gptk`. CRLF gives a black screen and
no log at all.

### 4. Fill in `port.json`

The [JSON generator](../../../tools/json-generator.md) builds the file. The
LÖVE-specific parts:

```json
"rtr": true,
"runtime": null,
"arch": ["aarch64", "x86_64"]
```

`rtr` is true only for games that need nothing from the user. `runtime` stays
empty because the LÖVE runtime ships with PortMaster itself.

### 5. Sort out the controls, then test

Most of the remaining work is [input](#input-and-controls). Test on more than
one resolution. The ports repo's contributor notes ask for 640x480 (the most
common), 1024x768, 1280x720 and 720x720, and optionally 320x240.

## Games the user supplies

Many LÖVE games are paid, and distributed as Windows `.exe` builds. Those are
fused, which means the `.exe` is a zip and a port can convert it on the user's
device. That keeps the game's files out of the port. For why PortMaster works
this way, see [the FAQ](../../../faq.md).

Set `rtr` to false and make `inst` say exactly which file to drop and where. For
Gravity Circuit it reads: drop `GravityCircuit.exe` from your Epic, GOG or Steam
copy into the `gamedata` folder.

There are two patterns, depending on how much work the conversion is.

### Unpack in the launch script

Shell Out Showdown is the simple case. The port folder holds an empty placeholder
named `place ShellOutShowdown.exe here`, so the user can see what's expected. The
script converts the `.exe` the first time it finds one:

```bash
if [ -f ShellOutShowdown.exe ]; then
  pm_message "Prepare game files ..."
  unzip ShellOutShowdown.exe -d ShellOutShowdown.love
  cp conf.lua ShellOutShowdown.love
  rm ShellOutShowdown.exe
fi

$LOVE_RUN "$GAMEDIR/ShellOutShowdown.love"
```

It unpacks into a directory (LÖVE runs a directory fine, whatever it's called),
copies the port's own `conf.lua` over the game's, and deletes the `.exe` so the
work only happens once. `pm_message` puts the text on screen.

You don't have to zip the result back into a `.love`. If you do need to replace a
file inside the game, such as `main.lua`, Pengu Never Left unpacks the `.exe`,
copies its own `main.lua` in, and zips the directory back up with `zip -0`,
which stores without compressing.

Several ports ship their own extractor rather than rely on the firmware having
one: Balatro bundles `7za`, and Braid and Beatblock bundle `unzip`. Bundled tools
need their license files in `licenses/` like everything else.

### Use the patcher

When the conversion takes a while, or needs real patching, use PortMaster's
patcher. It is itself a LÖVE app. It runs your patch script behind a dialogue
screen that tells the user what is happening, asks them to press A to begin, and
asks again to continue to the game once it finishes. Gravity Circuit runs it like
this:

```bash
GAMEFILE="./gamedata/GravityCircuit.exe"
if [ -f "$GAMEFILE" ]; then
  export PATCHER_FILE="$TOOLDIR/patchscript"
  export PATCHER_TIME="2-5 minutes"
  export controlfolder
  if [ -f "$controlfolder/utils/patcher.txt" ]; then
    $ESUDO chmod a+x "$TOOLDIR/patchscript"
    source "$controlfolder/utils/patcher.txt"
    pm_gptokeyb_finish
  else
    pm_message "This port requires the latest PortMaster to run, please go to https://portmaster.games/ for more info."
    sleep 5
    exit
  fi
fi
```

The check for `patcher.txt` matters: older PortMaster installs don't have it, and
this gives the user a message instead of a silent failure. Sourcing the file runs
the patcher through the same `love_11.5` runtime.

| Variable | What it does |
|---|---|
| `PATCHER_FILE` | The script to run. Required. |
| `PATCHER_TIME` | The estimate shown to the user, as free text. Defaults to "5 minutes". |
| `PATCHER_GAME` | The game's name in the dialogue. Defaults to "the game". Balatro sets it from the launcher's file name. |
| `PATCHER_QUESTIONS` | Optional. A Lua file of questions for the player to answer before the patch runs. |

The patcher can ask the player questions first. Arco asks whether to apply a
D-pad patch. The questions file returns a table, and each question has an `id`
and a list of `{value, label}` options:

```lua
return {
    {
        id = "DPADPATCH",
        question = "Do you want to apply the D-pad/L-stick L2 toggle patch? (Select Yes for D-pad only devices!)",
        options = {
            {"true", "Yes"},
            {"false", "No"}
        }
    }
}
```

It asks each one in turn, then runs the patch script with every answer set as an
environment variable named after its `id`, so this patch script reads
`$DPADPATCH`.

The patch script itself is ordinary bash. Gravity Circuit's unpacks the `.exe`
with a 7-Zip binary and deletes it, then applies a unified diff with a `patch`
binary the port ships for each architecture, from `bin.aarch64` and `bin.x86_64`:

```bash
cd ./gamedata
$GAMEDIR/bin.${DEVICE_ARCH}/patch -p1 < "$GAMEDIR/gravitycircuit.diff"
```

The original files have mixed line endings, so the script runs `dos2unix` over
every file the diff touches before patching. Without that, hunks fail to apply.

A diff is the right tool when you're changing the game's Lua. It stays small, it
doesn't contain the original code, and it fails loudly if the user has a version
you didn't expect.

Balatro goes further. It keeps a set of Lua patch files for the small-screen
layout, controls and performance, builds a patched copy of the game next to the
user's original, and rebuilds when a setting changes. Its script says as much
when something goes wrong: the purchased game was not modified. Leaving the
user's own file untouched and writing the result alongside it is a good habit.

## Input and controls

LÖVE reads gamepads itself, through SDL. So the first thing to find out is
whether the game does too. Search its source for `love.joystick`,
`gamepadpressed` or `joystickpressed`. Curse of the Arrow uses them, and so it
needs no mapping at all.

There are four situations, and real ports are spread across all of them.

**The game handles gamepads.** Run gptokeyb with no config:

```bash
$GPTOKEYB "$LOVE_GPTK" &
```

Without `-c`, [gptokeyb only acts as a tool to kill the
process](../packaging.md). The buttons reach the game through
`SDL_GAMECONTROLLERCONFIG`.

Layouts can still come out wrong. On some CFWs the A/B and X/Y buttons arrive
swapped relative to what the game expects. Shell Out Showdown swaps them for
ArkOS and ROCKNIX, and Max Payne for Knulli, by rewriting the controller mapping
before the game starts. Both ship a small script for it. PortMaster doesn't
provide one.

**The game is keyboard-only.** Map the buttons to keys with a `.gptk` file. The
first argument stays `$LOVE_GPTK`, and `-c` names the mapping:

```bash
$GPTOKEYB "$LOVE_GPTK" -c "./mrrescue.gptk" &
```

```ini
back = esc
start = enter
a = a
b = s
x = s
y = d
left = left
right = right
up = up
down = down
```

The [gptokeyb README](https://github.com/PortsMaster/gptokeyb) documents the
syntax.

**The game is mouse-driven.** gptokeyb can move the cursor, with the d-pad or
sticks, and click with the face buttons:

```ini
up = mouse_movement_up
down = mouse_movement_down
left = mouse_movement_left
right = mouse_movement_right
dpad_mouse_step = 6

a = mouse_left
b = mouse_right
y = mouse_slow
mouse_slow_scale = 50
```

A cursor that crosses a 640 pixel screen comfortably is too slow on a 1280 one.
Dumbass Smartass, Triple Trouble and several others compute the step from the
display width and write it into the `.gptk` before launch:

```bash
value=$(( 4 + (DISPLAY_WIDTH >= 640) + 2 * (DISPLAY_WIDTH >= 1280) + 3 * (DISPLAY_WIDTH >= 1920) ))
sed -i -E "s/(dpad_mouse_step|deadzone_scale) = [0-9]+/\1 = $value/g" "dumbasssmartass.gptk"
```

**The port uses gptokeyb2.** Six ports, among them Void Call and Ot, use
`$GPTOKEYB2` with an `.ini` instead. The idea is the same and the file format is
different:

```bash
$GPTOKEYB2 "$LOVE_GPTK" -c "./voidcall.ini" &
```

```ini
[controls]

back = esc
start = enter
a = z
b = x
y = c
```

## Resolution, conf.lua and performance

LÖVE reads `conf.lua` before it opens a window, so it's where window size,
fullscreen, the save identity and the target version are decided. A game written
for a desktop sometimes sets values that suit a monitor and not a handheld, and
then the port replaces the file:

- **Shell Out Showdown** ships its own complete `conf.lua`, with fullscreen on
  and a fixed `t.identity`, and copies it over the game's when it unpacks.
- **Planet D4RK** patches the game's `conf.lua` with a small diff instead of
  replacing it.

Setting `t.identity` yourself pins the name of the save folder, which stops saves
moving if the replacement `conf.lua` or the game changes.

The device's resolution is available to the launch script as `DISPLAY_WIDTH` and
`DISPLAY_HEIGHT`. A few ports use it to rewrite `conf.lua`. Nova Pinball does,
for one device:

```bash
if [ "$DEVICE_NAME" = "RGB30" ]; then
  sed -i 's/t.window.width = [0-9]*/t.window.width = '"$DISPLAY_WIDTH"'/' game/conf.lua
  sed -i 's/t.window.height = [0-9]*/t.window.height = '"$DISPLAY_HEIGHT"'/' game/conf.lua
fi
```

That is a fix for one device's quirk, not something to copy as a default. Most
ports don't touch resolution at all.

**Performance** is the other half. Per-frame effects that are free on a desktop
add up on a handheld GPU. Balatro asks on first launch whether to turn its CRT,
bloom, shadow and screen shake effects off, and whether to cap the frame rate at
60, 40 or 30. Players with performance to spare can keep every effect.

## Compatibility

Most LÖVE games port without modification. The things that cause trouble:

- **LÖVE version.** The runtime is 11.5. A game written for 0.x is not
  compatible with it, and the API changes between those versions are
  significant. Check `t.version` in `conf.lua`.
- **LuaJIT FFI and native C libraries.** Anything calling into a compiled `.so`
  needs that library rebuilt for aarch64 and x86_64, and shipped in the port.
  Put its folder on `LD_LIBRARY_PATH` before sourcing `love.txt`.
  `$LOVE_RUN` keeps your path and adds the runtime's. Don't bundle SDL2 or
  system libraries. Every CFW ships its own, and bundling them causes breakage
  you won't see on your own device.
- **Gamepad assumptions.** A game that only handles keyboard and mouse needs one
  of the mappings above.

## Ports that bundle their own LÖVE (legacy)

These ports predate the shared runtime. They're documented so you can read one.
A new port shouldn't be built this way.

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

`bin/love` is the executable and `libs/` holds what it links against. The launch
script adds `libs/` to `LD_LIBRARY_PATH` and runs the binary directly:

```bash
export LD_LIBRARY_PATH="$GAMEDIR/libs:$LD_LIBRARY_PATH"
$GPTOKEYB "love" -c "cityglitch.gptk" &
./bin/love "$launch_file"
```

Most of them ship `liblove-11.5.so`, the same version the runtime provides, so
there's no technical reason they carry it. A few differ. Thermomorph and UPO ship
11.4. Hawkthorne and Snowman Stack carry an unversioned `liblove.so.0` and set
`LOVE_GRAPHICS_USE_OPENGLES=1` before running it.

Some of these also offer armhf, by shipping a `love.armhf` next to the aarch64
binary. As noted above, armhf is being phased out.

## Tools

- [LÖVE](https://love2d.org/) is the framework itself, and the desktop build is
  useful for testing changes before putting them on a device. `love gamedata`
  runs a directory the same way `$LOVE_RUN` does.
- Any zip tool opens a `.love` archive or a fused `.exe`, since both are just
  zips.
- `dos2unix` for the line endings problem in Windows builds.

## Example ports

Real LÖVE ports in the library, useful to unpack and look at.

Ready to run on the shared runtime:

- [Curse of the Arrow](../../../../port/?name=curseofthearrow), a game that
  handles gamepads itself and needs no mapping
- [Mr. Rescue](../../../../port/?name=mrrescue) and
  [Friday Night Funkin](../../../../port/?name=fridaynightfunkin), keyboard
  games mapped with a `.gptk`
- [Dumbass Smartass](../../../../port/?name=dumbasssmartass), a mouse-driven
  game with the cursor speed scaled to the display
- [Ot](../../../../port/?name=ot), using gptokeyb2
- [Nova Pinball](../../../../port/?name=nova_pinball), rewriting `conf.lua` for
  one device

Games the user supplies:

- [Shell Out Showdown](../../../../port/?name=shelloutshowdown), unpacking a
  fused `.exe` in the launch script
- [Gravity Circuit](../../../../port/?name=gravitycircuit), using the patcher and
  a diff
- [Balatro](../../../../port/?name=balatro), with a rebuild-on-change patch
  system

A LÖVE launcher in front of another engine:

- [Max Payne](../../../../port/?name=maxpayne)

Bundling their own LÖVE binary, the older approach:

- [Blue Revolver](../../../../port/?name=bluerevolver)
- [City Glitch](../../../../port/?name=cityglitch)
- [Snowman Stack](../../../../port/?name=snowmanstack), on an older LÖVE build
