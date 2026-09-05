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

The runtime has to match the engine version the game was exported with. These
are the runtimes available, listed roughly most-used first, which is the best
available guide to what is known to work:

| Godot 3 (FRT) | Godot 4 |
|---|---|
| `frt_3.5.2` | `godot_4.3` |
| `frt_3.2.3` | `godot_4.5` |
| `frt_3.3.4` | `godot_4.2.2` |
| `frt_3.4.5` | `godot_4.4.1` |
| `frt_3.6` | `godot_4.4` |
| `frt_4.0.4` | `godot_4.6.3` |
| `frt_2.1.6` | `godot_4.7.1` |

`frt_3.5.2` is the most common runtime in the library by a wide margin. If a
Godot 3 game runs on it, that is the path of least resistance.

### Things that block a port

- **C# / Mono builds.** Godot games written in C# need the Mono-enabled engine
  build, which the standard runtimes are not. Very few ports manage this.
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

*Determining the exact minor version reliably still needs writing by someone who
does this regularly.* In practice porters often work down from the most common
runtimes, starting with `frt_3.5.2` for Godot 3.

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

**Exit shortcuts.** Set `FRT_NO_EXIT_SHORTCUTS` on FRT ports, or handheld button
combinations can quit the game unexpectedly.

**Resolution.** Godot 4 ports pass `--resolution` explicitly from
`$DISPLAY_WIDTH` and `$DISPLAY_HEIGHT` rather than letting the game choose.

**Rendering driver.** Godot 4 ports use `--rendering-driver opengl3_es`, since
handhelds provide OpenGL ES rather than desktop OpenGL.

**Save locations.** `XDG_DATA_HOME` is pointed at the port's own config folder
so the game writes saves inside the port rather than into the user's home
directory.

*A fuller list of recurring Godot bugs and their fixes still needs writing.*

## Tools

- [Godot](https://godotengine.org/) itself, for opening a project, checking a
  version, and re-exporting a pack where the game is open source.
- [FRT](https://github.com/efornara/frt) is the Godot 3 build for embedded ARM
  devices that the `frt_*` runtimes are made from.

## Example ports

Real Godot ports in the library, useful to unpack and look at:

- [ROTA](../../../../port/?name=rota)
- [Echo Chamber](../../../../port/?name=echo_chamber)
- [Dome Romantik](../../../../port/?name=domeromantik)
- [HELP! NO BRAKE](../../../../port/?name=help.no.brake)
