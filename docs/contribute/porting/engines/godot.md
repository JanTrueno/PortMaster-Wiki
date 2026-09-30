# Godot :simple-godotengine:

[Godot](https://godotengine.org/) is an open-source game engine used very widely
by indie developers. It's one of the most-ported engines in the library, behind
only GameMaker.

Godot games port well because the engine is open source. The game itself is a
data pack (`.pck`) plus an executable, and a Godot build made for ARM can run
that same data pack unmodified. In most cases the port ships only the `.pck` and
borrows the engine from a shared runtime.

!!! note "This guide is incomplete"
    The mechanism, compatibility and packaging sections are filled in from the
    port library. Identifying a game's exact engine version, and the list of
    known issues, still need input from someone who ports Godot games regularly.
    If that's you, the [Discord](https://discord.gg/eqjK6yNQS4) `#testing-n-dev`
    channel is the place to start.

## How PortMaster runs it

The two major Godot versions take different routes, and they are genuinely
different setups rather than two flavours of the same thing.

**Godot 3 runs on FRT**, a lightweight Godot 3 build for embedded and ARM
devices, and this is the more common of the two routes. The launch script mounts
the runtime squashfs, puts it on `PATH`, and hands the engine the game's pack:

```bash
runtime="frt_3.5.2"
godot_dir="$HOME/godot"
godot_file="$controlfolder/libs/${runtime}.squashfs"
$ESUDO mkdir -p "$godot_dir"
$ESUDO umount "$godot_file" || true
$ESUDO mount "$godot_file" "$godot_dir"
PATH="$godot_dir:$PATH"

export FRT_NO_EXIT_SHORTCUTS=FRT_NO_EXIT_SHORTCUTS
$GPTOKEYB "$runtime" -c "./portname.gptk" &
pm_platform_helper "$runtime"
"$runtime" $GODOT_OPTS --main-pack "gamedata/game.pck"
```

`FRT_NO_EXIT_SHORTCUTS` is set by nearly every FRT port. It stops FRT's built-in
key combinations from quitting the game, which would otherwise fire on handheld
button mappings.

**Godot 4 runs on a native `godot_4.x` runtime under weston.** Godot 4 ports
wrap the engine in weston, a Wayland compositor, because the Godot 4 renderer
needs a real display server rather than the bare framebuffer FRT is happy with.
FRT ports never use weston, so this is a clean dividing line between the two.

```bash
$ESUDO env $weston_dir/westonwrap.sh headless noop kiosk crusty_x11egl \
XDG_DATA_HOME=$CONFDIR $env_vars $godot_dir/$godot_executable \
--resolution ${DISPLAY_WIDTH}x${DISPLAY_HEIGHT} -f \
--rendering-driver opengl3_es --audio-driver ALSA \
--main-pack $GAMEDIR/$pck_filename
```

The practical consequence is that Godot 4 ports are heavier and have more that
can go wrong. Godot 3 is the smoother target where you have the choice.

## Compatibility

The runtime has to match the major engine version the game was exported with. These
are the runtimes currently available, listed roughly most-used first:

| Godot 3 (FRT) | Godot 4 |
|---|---|
| `frt_3.5.2` | `godot_4.3` |
| `frt_3.2.3` | `godot_4.5` |
| `frt_3.3.4` | `godot_4.2.2` |
| `frt_3.4.5` | `godot_4.4.1` |
| `frt_3.6` | `godot_4.4` |
| `frt_4.0.4` | `godot_4.6.3` |
| `frt_2.1.6` | `godot_4.7.1` |

### Things that block a port

- **C# / Mono builds.** Godot games written in C# need the Mono-enabled engine
  build, which is only available for later versions (4.2.2 onwards).
- **GDNative / GDExtension plugins.** These are compiled native libraries. They
  have to be rebuilt for ARM, and if the source isn't available the game can't
  be ported.
- **Godot 4 rendering requirements.** Godot 4's renderer is more demanding than
  Godot 3's, which is what the weston wrapper and the `opengl3_es` driver exist
  to work around. Lower-end devices struggle regardless.

## Identifying a game

You need the major version first, since that decides whether you're targeting
FRT or a Godot 4 runtime, and then the specific engine version to pick a
runtime.

The `.pck` file and the game executable both carry version information, and the
engine binary shipped with a desktop build reports it with `--version`.

For a more detailed version number, you can use [GDRETools](https://github.com/GDRETools/gdsdecomp):
- Load the game data (pck if available, otherwise it's safe to assume data was embeded in the exe) in GDRE.
- Look at the top left corner: you should be able to see a label indicating something like "Version: 4.3.0", that is this game's godot version! 

## Port structure

Godot ports are unusually small, because the engine lives in the shared runtime
and the port carries little more than the data pack:

```
A Meta Data Game.sh
ametadatagame/
├── gamedata/
│   └── a_meta_data_game.pck
├── ametadatagame.gptk
└── LICENSE.txt
```

**`gamedata/`** holds the `.pck`, the packed data file Godot exports. This is
the whole game: scenes, scripts, assets.

**`portname.gptk`** holds the gptokeyb mapping, so controller input reaches a
game that expects keyboard and mouse.

Godot 4 ports follow the same shape but additionally depend on the weston
runtime, and some carry mod-loader setup or per-port config alongside the pack.

## Patching and common fixes

### No pck in my game

If there is no pck to be found, however you are certain that this is a Godot game, you try to load the exe into GDRE instead, if that works, great! It means that the pck is embedded inside your executable, you can freely point to the exe in that case instead of a pck, the runtime will identify it and proceed normally.

### General export variables

**Exit shortcuts.** Set `FRT_NO_EXIT_SHORTCUTS` on FRT ports, or handheld button
combinations can quit the game unexpectedly.

**Resolution.** Godot 4 ports pass `--resolution` explicitly from
`$DISPLAY_WIDTH` and `$DISPLAY_HEIGHT` rather than letting the game choose.

**Rendering driver.** Godot 4 ports use `--rendering-driver opengl3_es`, since
handhelds provide OpenGL ES rather than desktop OpenGL.

**Save locations.** `XDG_DATA_HOME` is pointed at the port's own config folder
so the game writes saves inside the port rather than into the user's home
directory.

### Double Inputs.

Some later Godot versions suffer from double inputs: meaning that the engine will identify a wrong gamepad profile, that is inconsistent across devices.
Therefore the port should either patch out gamepad controls by decompiling the game or block them with libcrusty:

*For westonpack ports:*
```
$ESUDO env WRAPPED_PRELOAD_PANFROST=$GAMEDIR/libcrusty.so CRUSTY_BLOCK_INPUT=1 $weston_dir/westonwrap.sh headless noop kiosk crusty_x11egl \
XDG_DATA_HOME=$CONFDIR $godot_dir/$godot_executable \
--resolution ${DISPLAY_WIDTH}x${DISPLAY_HEIGHT} -f --disable-cursor \
--rendering-driver opengl3_es --audio-driver ALSA --main-pack $GAMEDIR/$pck_filename
```
*For frt ports:*
```
export FRT_NO_EXIT_SHORTCUTS=FRT_NO_EXIT_SHORTCUTS
export CRUSTY_BLOCK_INPUT=1
$GPTOKEYB "$runtime" -c "./portname.gptk" &
pm_platform_helper "$runtime"
LD_PRELOAD="$GAMEDIR/libcrusty.so" "$runtime" $GODOT_OPTS --main-pack "gamedata/game.pck"
```
note that you will need to add libcrusty in your port directory [(example: merp in merpworld)](https://github.com/PortsMaster/PortMaster-New/tree/main/ports/merpinmerpworld/merpinmerpworld)

### Precomputed patches (xdelta)

Build the modified game file on a PC, ship the binary difference, and apply it
on device at first launch.
[XDelta3](https://github.com/Moodkiller/xdelta3-gui-2.0) creates the patch from
the difference between the original and modified files, and the `xdelta3` binary
in the PortMaster control folder applies it.

```bash
# Check if pck exists and its MD5 checksum matches, then apply the patch
if [ -f "gamedata/a_meta_data_game.pck" ]; then
    checksum=$(md5sum "gamedata/a_meta_data_game.pck" | awk '{print $1}')
        if [ "$checksum" = "4b97bb2da8c515d787fe70aa03550ce5" ]; then
        $ESUDO $controlfolder/xdelta3 -d -s "gamedata/a_meta_data_game.pck" -f "./patch/patch.xdelta3" "gamedata/a_meta_data_game_patched.pck" && \
        rm "gamedata/a_meta_data_game.pck"
    fi
fi
```

This is simple and fast, but the patch is tied to one exact build of the game, and will fail if the game updates.
*Also note that Godot xdelta patches can get very big, so should be generally avoided*

*A fuller list of recurring Godot bugs and their fixes still needs writing.*

## Tools

- [Godot](https://godotengine.org/) itself, for opening a project, checking a
  version, and re-exporting a pack where the game is open source.
- [FRT](https://github.com/efornara/frt) is the Godot 3 build for embedded ARM
  devices that the `frt_*` runtimes are made from.
- [GDRE tools](https://github.com/GDRETools/gdsdecomp) is used to check engine version number, and decompile the game in ports that require changing the game's source.

## Example ports

Real Godot ports in the library, useful to unpack and look at:

- [ROTA](../../../../port/?name=rota)
- [Echo Chamber](../../../../port/?name=echo_chamber)
- [Dome Romantik](../../../../port/?name=domeromantik)
- [HELP! NO BRAKE](../../../../port/?name=help.no.brake)
