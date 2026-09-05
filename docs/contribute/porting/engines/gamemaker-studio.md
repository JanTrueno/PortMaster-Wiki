# GameMaker Studio :simple-gamemaker:

[GameMaker Studio](https://gamemaker.io/en) is a 2D game engine built around a
drag-and-drop editor and its own scripting language, GML. It exports to Windows,
macOS, Linux, Android, iOS and the major consoles.

It does not export to ARM Linux, and that is the whole problem. A GameMaker game
has no build that runs natively on the handhelds PortMaster targets, so every
GameMaker port goes through a compatibility layer instead.

It is still the most-ported engine in the library by a wide margin.

## How PortMaster runs it

[GMLoader](https://github.com/JohnnyonFlame/droidports) and its successor
[GMLoaderNext](https://github.com/JohnnyonFlame/gmloader-next), written by
[JohnnyOnFlame](https://github.com/JohnnyonFlame) and contributors, are
GameMaker compatibility layers for ARM Linux. They share a codebase and history
with the PS Vita project
[YoYoLoader](https://github.com/Rinnegatamante/yoyoloader_vita).

Both wrap `libyoyo.so`, the official GameMaker runner for Android. They load
that ARM executable into memory, resolve its imports against native functions,
and patch it where needed so it runs. The effect is a minimal Android-like
environment in which an Android GameMaker build executes directly on ARM Linux.

Most GameMaker ports now use GMLoaderNext. The rest still run on the original
GMLoader.

The [research documentation](https://github.com/JohnnyonFlame/yyg_fix/blob/master/RESEARCH.md)
covers the origin and the deeper technical detail.

## Compatibility

GameMaker can compile a game two ways, and only one of them ports. Bytecode
builds are portable; YoYo Compiler (YYC) builds compile GML straight to machine
code, which is faster and harder to tamper with but ties the game to the
platform it was built for.

Since the loader runs the Android runner, an Android build is what's needed:

| Platform | Bytecode compiler | YoYo Compiler (YYC) |
|----------|-------------------|---------------------|
| Android  | Yes               | Yes                 |
| Windows  | Yes               | No                  |
| Linux    | Yes               | No                  |
| macOS    | Yes               | No                  |

Which loader applies depends on the GameMaker version and the device
architecture:

| Loader | GameMaker versions | Architecture |
|---|---|---|
| `gmloader` | 2022.x and earlier | ARMv7 / armhf |
| `gmloadernext.armhf` | all | ARMv7 / armhf |
| `gmloadernext.aarch64` | 2.2.1 and later | ARMv8 / aarch64 |

GMLoader is deprecated. Use it only when nothing else works.

## Identifying a game

Two facts decide everything else: the GameMaker version, and whether the game
was built as bytecode or YYC.

[UndertaleModTool](https://github.com/UnderminersTeam/UndertaleModTool/releases)
answers both. Open the game's data file, which will be `data.win`, `game.unx`,
`game.ios` or `game.droid`, extracting it from an APK or the game folder first
if needed:

- The version is under **Data > General Info**.
- A warning appears on load if the game uses YYC.

UndertaleModTool makes an educated guess at the version, so treat it as
approximate rather than authoritative.

For finding candidates in the first place,
[itch.io](https://itch.io/games/made-with-gamemaker) and
[SteamDB](https://steamdb.info/tech/Engine/GameMaker/) both list games by
engine. Free games are the better starting point, since most of the
commercially successful portable ones are already ported.

## Wrappers

The loader needs a wrapper APK carrying the GameMaker runtime libraries for the
target architecture, and those libraries have to match the loader you picked:
ARMv7 libraries for `armhf`, ARMv8 for `aarch64`.

Prebuilt wrappers are available from the
[GMloader-ports repository](https://github.com/Fraxinus88/GMloader-ports/tree/main/gmloader%20wrappers%20(APK)).

For final packaging we prefer building a custom wrapper: download the matching
GameMaker Studio version, set up the Android export, export an open-source
example, launch it once, then strip the assets back out.

```bash
zip -d portname.port 'assets/*'
```

## Port structure

```
Portname.sh
portname/
├── lib/
│   ├── armv8a/
│   ├── armv7a/
│   ├── libopenal.so.1
│   ├── libzip.so.5
│   └── libcrypto.so.1
├── assets/
│   └── .gitkeep
├── saves/
│   └── .gitkeep
├── gmloader.json
├── patches/
│   └── patchscript
├── portname.gptk
└── portname.port
```

**`lib/`** holds Android AOSP libraries taken from a prebuilt image provided by
Google. It's named `lib` because these are native Android libraries and this is
the path structure Android uses. The `libs.${DEVICE_ARCH}` folder contains
libraries native to either `aarch64` or `armhf`. GMLoaderNext needs at minimum
`libcrypto`, `libopenal` and `libzip`.

**`licenses/`** contains the license agreements for each library and binary used
in GMLoader.

**`assets/`** is where the end user puts their game data, typically everything
from a Steam or GOG install folder, or the contents of an itch.io archive. Once
`patchscript` has finished on first run, this folder can be removed.

**`saves/`** holds the game's save data. The name is conventional rather than
required.

**`gmloader.json`** carries per-port configuration for GMLoaderNext. It can be
renamed to `portname.json`.

```json
{
    "save_dir": "saves",
    "apk_path": "my_game.port",
    "show_cursor": false,
    "disable_controller": false,
    "force_platform": "os_windows"
}
```

**`patches/patchscript`** is a bash script run on first boot by the PortMaster
patcher. It deliberately avoids the `.sh` extension so it doesn't interfere with
PortMaster's own scripts. There's a
[worked example](https://github.com/JeodC/PortMaster-UFO50/blob/main/ufo50/tools/patchscript)
to work from.

**`portname.gptk`** holds the gptokeyb mapping. Include an empty one even when
the game has native gamepad support, since it helps with debugging.

```
back = \"
start = \"
up = \"
down = \"
left = \"
right = \"
a = \"
b = \"
x = \"
y = \"
l1 = \"
l2 = \"
l3 = \"
r1 = \"
r2 = \"
r3 = \"
left_analog_up = \"
left_analog_down = \"
left_analog_left = \"
left_analog_right = \"
right_analog_up = \"
right_analog_down = \" 
right_analog_left = \"
right_analog_right = \"
```

**`portname.port`** is an archive structured like an APK but without the
Android-specific references. It contains a `lib` folder with the GameMaker
runtime, and once the port is packed, an `assets` folder holding the game data
that was previously in `portname/assets`.

!!! note "Why the game data is bundled this way"
    GameMaker's [free](https://gamemaker.io/en/legal/gamemaker-runtime-licence-free)
    and [professional](https://gamemaker.io/en/legal/gamemaker-runtime-licence-professional)
    runtime licences both state that the runtime may be distributed
    "as an integrated and inseparable part of your content". Bundling the game
    data with the runtime inside `portname.port` is our good-faith way of
    meeting that condition.

## Patching and common fixes

Most GameMaker ports need the game's data file modified before it runs properly
on a handheld. There are two ways to ship those modifications, and newer ports
increasingly use the second.

### Precomputed patches (xdelta)

Build the modified data file on a PC, ship the binary difference, and apply it
on device at first launch.
[XDelta3](https://github.com/Moodkiller/xdelta3-gui-2.0) creates the patch from
the difference between the original and modified files, and the `xdelta3` binary
in the PortMaster control folder applies it.

```bash
# Check if "data.win" exists and its MD5 checksum matches, then apply the patch
if [ -f "assets/data.win" ]; then
    checksum=$(md5sum "assets/data.win" | awk '{print $1}')
        if [ "$checksum" = "4b97bb2da8c515d787fe70aa03550ce5" ]; then
        $ESUDO $controlfolder/xdelta3 -d -s "assets/data.win" -f "./patch/patch.xdelta3" "assets/game.droid" && \
        rm "assets/data.win"
    fi
fi
```

This is simple and fast, but the patch is tied to one exact build of the game,
which is why the checksum guard is there.

### On-device patching (UndertaleModCli)

The newer approach runs UndertaleModTool's command line interface,
`UndertaleModCli.dll`, on the handheld itself through .NET. The port ships the
transformation rather than the result, so it works from whatever copy of the
game the user actually owns.

It needs two runtimes, declared in the port's `port.json` and mounted by the
patchscript before use. `gmtoolkit.squashfs` provides `utmt-cli` and `gmtools`;
`dotnet-8.0.12.squashfs` provides `dotnet` itself.

```bash
TOOLKIT="$HOME/gmtoolkit"
RUNTIME="$controlfolder/libs/gmtoolkit.squashfs"
if [ -f "$RUNTIME" ]; then
    $ESUDO mkdir -p "$TOOLKIT"
    $ESUDO umount "$TOOLKIT" 2>/dev/null || true
    $ESUDO mount "$RUNTIME" "$TOOLKIT"
else
    echo "This port requires the GMToolkit runtime. Please download it."
    sleep 2
    patch_failure
fi
```

The dotnet runtime is mounted the same way, from
`$controlfolder/libs/dotnet-8.0.12.squashfs` onto `$HOME/mono`. Three
UndertaleModCli verbs cover nearly every port.

**`dump`** externalises the game's textures and writes out a converted data
file. This is the most common use by a wide margin, since it both compresses
textures and produces the `game.droid` the loader wants.

```bash
dotnet "$TOOLKIT/utmt-cli/UndertaleModCli.dll" \
    dump "$DATADIR/data.win" \
    -e "$DATADIR/textures" "$DATADIR/game.droid"
```

**`load -s`** runs a UndertaleModTool C# script (`.csx`) against the data file,
which is how the UTMT scripts below get applied on device rather than by hand.

```bash
dotnet "$TOOLKIT/utmt-cli/UndertaleModCli.dll" \
    load "$DATADIR/data.win" \
    -s "$GAMEDIR/tools/NewTextureRepacker.csx" -o "$DATADIR/data2.win"
```

**`replace`** swaps out GML code entries from `.gml` files shipped in the port,
which is the cleanest way to change game logic without carrying a whole patched
data file.

```bash
CODEARGS=()
for file in "$GAMEDIR/tools/gml/"*.gml; do
    [ -f "$file" ] || continue
    entry=$(basename "$file" .gml)
    CODEARGS+=(--code "$entry=$file")
done

dotnet "$TOOLKIT/utmt-cli/UndertaleModCli.dll" \
    replace "$DATADIR/data.win" -o "$DATADIR/data2.win" "${CODEARGS[@]}"
```

Patching this way takes noticeably longer than applying an xdelta, so use the
PortMaster patching program to show progress.

### Packing audio into the wrapper

GMLoader can have trouble loading audio that isn't packed into the wrapper APK.
This packs the OGGs in, and can be adapted for games that use audiogroups.

```bash
# Check for .ogg files and move to APK
if [ -n "$(ls ./assets/*.ogg 2>/dev/null)" ]; then
    zip -r -0 ./portname.port ./assets/
    echo "Zipped contents to ./portname.port"
else
    echo "No .ogg files found"
fi
```

### NewTextureRepacker

A texture export and repack script by JohnnyOnFlame, shipped as a `.csx` and run
through `load -s`. Fixes crashes caused by oversized texture pages on Mali GPUs,
fixes broken fonts on the same, and reduces RAM usage.

### Bytecode up/downgraders

UndertaleModTool scripts that move a game between bytecode versions, which can
improve compatibility for GMS1 and GMS2 games.

### GMTools

GameMaker games handle audio in several ways: streamed externally like
Undertale, grouped into `audiogroup.dat` files, or embedded in the data file.
Anything not streamed gets loaded into memory at runtime, which is a problem on
low-memory handhelds. [GMTools](https://github.com/cdeletre/gmtools) analyses
the audiogroups and the data file, converts any `.wav` it finds to `.ogg`, and
can compress to a target bitrate. The RAM saving is significant, and audio
quality matters little through handheld speakers. It ships inside the
`gmtoolkit` runtime alongside `utmt-cli`.

## Tools

- [GameMaker Studio](https://gamemaker.io/en) is the engine itself. If a game is
  open source we can build it directly and make the port Ready to Run, as with
  [Spelunky Classic HD](https://github.com/JanTrueno/SpelunkyClassicHD).
- [UndertaleModTool](https://github.com/UnderminersTeam/UndertaleModTool)
  examines and modifies GameMaker data files (`data.win`, `game.unx`,
  `game.ios`, `game.droid`) via scripts. Its command line interface,
  `UndertaleModCli`, is what runs on-device in newer ports.
- [XDelta3 GUI](https://github.com/Moodkiller/xdelta3-gui-2.0) creates `.xdelta`
  patch files from the difference between two data files. A CLI variant ships
  with PortMaster to apply them to legally obtained game files.
- [GMTools](https://github.com/cdeletre/gmtools), by PortMaster crew member
  Cyril (kotzebuedog), handles audio analysis and compression.
- [GMLoader](https://github.com/JohnnyonFlame/droidports) and
  [GMLoaderNext](https://github.com/JohnnyonFlame/gmloader-next) are the
  compatibility binaries themselves, for armhf and aarch64 respectively.

## Building GMLoaderNext from source

!!! info
    Only needed for development and contribution. Prebuilt binaries ship in the
    example packages.

Clone the repository with its submodules:

```bash
git clone https://github.com/JohnnyonFlame/gmloader-next --recursive
```

Build for the target platform:

```bash
make -f Makefile.gmloader ARCH=aarch64-linux-gnu
```

Building on Debian Bullseye for older platforms:

```bash
make -f Makefile.gmloader \
ARCH=aarch64-linux-gnu \
LLVM_FILE=/usr/lib/llvm-11/lib/libclang-11.so.1 \
LLVM_INC=/usr/aarch64-linux-gnu/include/c++/10/aarch64-linux-gnu \
-j$(nproc)
```

Generate the libc dependencies:

```bash
python3 scripts/generate_libc.py aarch64-linux-gnu \
--llvm-includes /usr/aarch64-linux-gnu/include/c++/10/aarch64-linux-gnu \
--llvm-library-file "/usr/lib/llvm-11/lib/libclang-11.so.1"
```

Then copy the redistributable libraries into the application directory:

```bash
cp -r lib_redist/ <application_folder>/
```

The [project documentation](https://github.com/JohnnyonFlame/gmloader-next) has
the full detail.

## Example ports

Real GameMaker ports in the library, useful to unpack and look at:

- [Undertale](../../../../port/?name=undertale)
- [AM2R](../../../../port/?name=am2r)
- [Deltarune](../../../../port/?name=deltarune)
- [Pizza Tower](../../../../port/?name=pizzatower)
- [Forager](../../../../port/?name=forager)
- [Downwell](../../../../port/?name=downwell)
- [Risk of Rain (2013)](../../../../port/?name=riskofrain)
