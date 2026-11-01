# FNA :material-controller:

[FNA](https://github.com/FNA-XNA/FNA) is an open-source reimplementation of
XNA 4, Microsoft's C# game framework. Many indie games from the XNA era and
after run on it, and it's the framework behind more than twenty ports in the
library, among them Celeste, Axiom Verge, TowerFall, Rogue Legacy, Bleed and
Blossom Tales II.

An FNA game is a .NET assembly, not native code. It runs on Mono, next to FNA's
own native libraries: FNA3D for graphics and FAudio for audio. That makes these
ports heavier to set up than most, and it's why much of this page is about
patching. A lot of FNA games need their own code changed before they run well
on a handheld.

!!! note "FNA, XNA and MonoGame are different things"
    **XNA 4** is Microsoft's original framework, long discontinued. Games built
    on it reference `Microsoft.Xna.Framework*` assemblies and expect Windows.
    **FNA** reimplements the same API on SDL so those games can run elsewhere,
    and it's what this page covers. **MonoGame** is a separate, independent
    reimplementation with its own content pipeline and additions to the API.
    A game ships one of them, and the approach for a port depends on which, so
    don't mix advice between them. Stardew Valley is a MonoGame game, and it
    doesn't follow this page.

!!! note "This guide is incomplete"
    The Mono route, patching and texture sections come from working ports. Two
    things are still missing. Every FNA port today runs on Mono, and none uses
    the `dotnet` runtime, so there is no documented route yet for an FNA game
    built on modern .NET. The ASTC support described below lives in custom FNA
    and FNA3D builds, not in upstream FNA.

## How PortMaster runs it

FNA games run on **Mono**, using the `mono-6.12.0.122-aarch64.squashfs` runtime.
That is the only Mono runtime PortMaster has, and it only has an aarch64 build,
so FNA ports are aarch64-only.

```json
"runtime": ["mono-6.12.0.122-aarch64.squashfs"],
"arch": ["aarch64"]
```

A port has two layers, found in two different ways:

- **Managed**: `FNA.dll`, the SDL2 bindings (`SDL2-CS.dll`) and the game itself.
  Mono finds these through `MONO_PATH`.
- **Native**: `libFNA3D`, `libFAudio`, `libtheorafile` and any other `.so` the
  game needs. The dynamic linker finds these through `LD_LIBRARY_PATH`.

SDL2 itself isn't in either list. Every CFW ships its own, and ports must not
bundle it.

The launch script mounts the runtime, points Mono at the port's files, and
starts the game's `.exe` through `mono`. This is based on Axiom Verge's, with
Mono's own `lib/` folder added to `LD_LIBRARY_PATH`:

```bash
GAMEDIR="/$directory/ports/axiom-verge"
cd "$GAMEDIR/gamedata"

> "$GAMEDIR/log.txt" && exec > >(tee "$GAMEDIR/log.txt") 2>&1

# Setup mono
monodir="$HOME/mono"
monofile="$controlfolder/libs/mono-6.12.0.122-aarch64.squashfs"
$ESUDO mkdir -p "$monodir"
$ESUDO umount "$monofile" || true
$ESUDO mount "$monofile" "$monodir"

# Setup savedir
bind_directories ~/.local/share/AxiomVerge "$GAMEDIR/savedata"

# Remove all the dependencies in favour of system libs
rm -f System*.dll mscorlib.dll FNA.dll Mono.*.dll

export MONO_PATH="$GAMEDIR/dlls"
export LD_LIBRARY_PATH="$GAMEDIR/libs:$monodir/lib:$LD_LIBRARY_PATH"
export PATH="$monodir/bin:$PATH"

export FNA3D_FORCE_DRIVER=OpenGL
export FNA3D_OPENGL_FORCE_ES3=1

$GPTOKEYB "mono" &
$TASKSET mono AxiomVerge.exe

$ESUDO umount "$monodir"
pm_finish
```

What the less obvious parts do:

- **The `squashfs` mount** is how a runtime gets used: it's mounted at
  `$HOME/mono` for the run and unmounted at the end. The `umount ... || true`
  beforehand clears a mount left over from a crashed run.
- **`rm -f System*.dll mscorlib.dll FNA.dll Mono.*.dll`** deletes the copies of
  those assemblies that shipped with the game, so the runtime's own and the
  port's `FNA.dll` in `dlls/` are the ones used. Without it a Windows build's
  copies can win.
- **`$GPTOKEYB "mono"`** names `mono` as the process to kill, because that is
  what is running. It has no config: see [Input and saves](#input-and-saves).
- **`$TASKSET`** comes from `tasksetter`, which the launch script sources near
  the top (`source $controlfolder/tasksetter`). It pins the game to the fastest
  CPU cores when `taskset` is available and expands to nothing otherwise.
- **`$monodir/lib` on `LD_LIBRARY_PATH`** is needed for ahead-of-time
  compilation, covered [below](#ahead-of-time-compilation).

The variables ports set, in rough order of how often:

| Variable | What it does |
|---|---|
| `MONO_PATH` | Where Mono looks for the managed assemblies. Nearly every port points it at `dlls/`. |
| `LD_LIBRARY_PATH` | Where the native `.so` files live: the port's `libs/`, and Mono's own `lib/`. |
| `FNA3D_FORCE_DRIVER=OpenGL` | Pins FNA3D to its OpenGL driver instead of probing for others. |
| `FNA3D_OPENGL_FORCE_ES3=1` | Makes FNA3D ask for an OpenGL ES 3 context, which is what the handheld drivers provide. Nearly every port sets it. |
| `FNA3D_OPENGL_FORCE_VBO_DISCARD=1` | Set by about fifteen ports. Upstream FNA3D has no hint by this name, so on a stock build it does nothing. |
| `FNA_PLATFORM_BACKEND=SDL2` | Selects FNA's SDL2 backend. See [SDL2 and SDL3](#fna-versions-sdl2-and-sdl3). |
| `FNA_SDL2_FORCE_BASE_PATH=0` | Eight ports set it. Old name for `FNA_SDL_FORCE_BASE_PATH`, still accepted. At 0, which is also the default, FNA uses the CLR's base directory instead of SDL's. |
| `MONO_GC_PARAMS` | Tunes the garbage collector. Rogue Legacy and Wizorb use `major=marksweep,nursery-size=32m`. |
| `MONO_IOMAP=all` | Mono's path-mapping switch for Windows-style paths and case differences. Eight ports set it. Whether it still has any effect on Mono 6.12 hasn't been checked. |
| `SDL_NO_SIGNAL_HANDLERS=1` | Stops SDL installing its own signal handlers. Set by five recent ports. |
| `SDL_TOUCH_MOUSE_EVENTS=0`, `SDL_MOUSE_TOUCH_EVENTS=0` | Stops SDL turning touch into mouse input and the reverse, for handhelds with a touchscreen. |

Most ports need only the first five. The rest are fixes for one game.

## FNA versions, SDL2 and SDL3

A game's `FNA.dll` fixes which FNA it uses, and the native libraries have to
come from the matching release. FNA pins FNA3D, FAudio and Theorafile as
submodules under `lib/`, and its releases move them together (the commit titled
"FAudio/FNA3D 25.03" bumps the FAudio and FNA3D submodules). Mixing a newer
FNA3D with an older `FNA.dll` can fail in ways that look like unrelated bugs.

What's in the library now spans several eras:

- Older ports ship `OpenAL-CS.dll`, from before FNA used FAudio.
- Axiom Verge ships FNA3D and FAudio 22.03 (`libFNA3D.so.0.22.03`).
- Newer FNA builds exist too, which is where SDL comes in.

**FNA 25.03 made SDL3 the default.** FNA, FNA3D and FAudio all moved to it, and
handhelds ship SDL2. A current FNA still builds for SDL2, but you have to ask.
There are two switches, and they must agree:

1. **Build the natives against SDL2.** FNA3D and FAudio both have a CMake
   option for it, on by default:

    ```bash
    cmake -B build -DBUILD_SDL3=OFF
    cmake --build build
    ```

    Build for aarch64 on an aarch64 machine or with a cross toolchain.

2. **Tell FNA to use the SDL2 backend at runtime.** FNA compiles in both
   backends and chooses at startup, so no rebuild of `FNA.dll` is needed:

    ```bash
    export FNA_PLATFORM_BACKEND=SDL2
    ```

An FNA from before 25.03 only has SDL2 and ignores the variable, which is why
setting it is harmless in older ports. The old `FNA_SDL2_FORCE_BASE_PATH` is
copied across to `FNA_SDL_FORCE_BASE_PATH` for you, so scripts written for one
still work with the other.

Some games ship their own modified FNA. If a game's fork changes the API, such
as making `ContentManager.Load<T>` return `object`, then stock FNA won't bind to
it. Rebuild the game's variant instead of swapping in the current release.

FAudio's SDL2 platform needed one fix on a Rockchip handheld whose audio
backend was half set up: PipeWire present but its `client.conf` missing. FAudio's
call to `SDL_GetDefaultAudioInfo` crashes inside SDL2 there, and it's a hard
crash, not an error code. Skipping the call and starting from an empty format,
which falls back to 48000 Hz stereo, avoids it. A custom FAudio build is
currently the only way to get that fix.

## Identifying a game

Look at what sits next to the game's `.exe`, and at what the `.exe` references:

- **`FNA.dll`**, often with native `FNA3D`, `FAudio` and `SDL2` libraries, means
  the game already runs on FNA.
- **`Microsoft.Xna.Framework*` references** in the `.exe`, with no such DLLs in
  the folder, mean XNA 4. Those assemblies normally come from the XNA
  redistributable on the user's PC. Open the `.exe` in a decompiler such as
  ILSpy and read its assembly references.
- **`MonoGame.Framework.dll`** means MonoGame.

Then check the rest before you commit to a port:

- **The .NET target.** Mono 6.12 runs .NET Framework assemblies. A game built for
  modern .NET doesn't run on it.
- **Windows-only dependencies.** WinForms, GDI+, DirectInput, SlimDX (the real
  one is C++/CLI and can't load under Mono) and Windows-only native DLLs all
  need a stub or a patch.
- **Single-file bundles.** Some games ship as an Enigma Virtual Box bundle, one
  `.exe` that holds the real game and its files. `evbunpack` extracts it, and
  FNAPatches has a Mono-loadable `EVBUnpack.exe` so a port can unpack on the
  device instead of asking the player to do it on a PC.
- **Content and audio.** `.xnb` files are compiled content. XACT banks (`.xwb`,
  `.xsb`) are handled by FAudio. FMOD banks need the FMOD libraries, see
  [below](#audio-video-and-middleware).

XNA 4 games can run on FNA without being recompiled. The game's references to
`Microsoft.Xna.Framework*` are satisfied by stub assemblies that forward every
type to FNA. Under Mono nothing else is needed. Blossom Tales runs this way, with
managed stubs standing in for SlimDX and Steamworks.NET too, see [Audio, video
and middleware](#audio-video-and-middleware) below.

## Port structure

This is the layout of a current port. Axiom Verge:

```
Axiom Verge.sh
axiom-verge/
├── dlls/
│   ├── FNA.dll
│   ├── FNA.dll.so
│   ├── SDL2-CS.dll
│   ├── SDL2-CS.dll.so
│   └── SDL2-CS.dll.config
├── libs/
│   ├── libFNA3D.so.0
│   ├── libFAudio.so.0
│   ├── libtheorafile.so
│   └── libsteam_api.so
├── gamedata/
├── savedata/
└── licenses/
    ├── fna.LICENSE
    ├── mono.LICENSE
    └── ...
```

- **`dlls/`** holds the managed side: FNA, its SDL bindings, and the
  `.dll.so` files described under [ahead-of-time
  compilation](#ahead-of-time-compilation). The `.config` files hold the
  `dllmap` entries that tell Mono which native library a name resolves to.
- **`libs/`** holds the native side, plus any stubs for libraries the game
  expects.
- **`gamedata/`** is the game. Either the user supplies it, or it's included for
  free or demo games.
- **`savedata/`** is where saves end up, see [Input and saves](#input-and-saves).
- **`licenses/`** has one file per component. FNA ports typically carry FNA, Mono,
  MonoXNA, lzxdecoder, Theorafile, libtheora, libogg and libvorbis, plus the
  game's own.

## Games the user supplies

Most FNA games are commercial, so most FNA ports follow the same shape: the port
holds the patches and tools, the player copies in the game, and a first-run step
prepares it.

Rogue Legacy shows the pieces. The port holds a placeholder file named `PLACE
CONTENT FOLDER HERE.txt` that says exactly what to copy and what the folder must
be called. The script refuses to go on without it:

```bash
if [ ! -d "$GAMEDIR/gamedata/Content" ]; then
    pm_message "Content folder missing! Copy your legally-owned Content/ folder into $GAMEDIR/gamedata/ and try again."
    sleep 5
    exit 1
fi
```

It then runs PortMaster's patcher once, guarded by a marker file that the
patch script creates when it finishes:

```bash
if [ ! -f "$GAMEDIR/patch_completed" ]; then
    export PATCHER_FILE="$GAMEDIR/tools/patchscript"
    export PATCHER_GAME="Rogue Legacy"
    export PATCHER_TIME="about 5 to 10 minutes"
    source "$controlfolder/utils/patcher.txt"
fi
```

The patcher is documented in the [LÖVE guide](love2d.md#use-the-patcher), since
it is itself a LÖVE app. Everything on this page that happens "on first launch"
runs inside a patch script like this. Other ports use a plain script instead: Bleed
prints to the console, and Celeste runs its repacker behind a progress screen.

## Audio, video and middleware

**FAudio** plays XNA's audio, including XACT banks. **Theorafile**
(`libtheorafile.so`) decodes the Ogg Theora video that many FNA games use for
cutscenes.

**FMOD** is a separate matter. Several FNA games use it instead of XACT, and
there are two generations, handled differently.

*FMOD Studio 1.x (Celeste).* The game calls FMOD Studio 1.x, and handhelds have
the 2.x libraries. `fmodstudio_fix.so`, from FNAPatches, bridges the two: it
forwards the calls whose signatures changed, such as
`FMOD_Studio_EventInstance_SetParameterValue` to `SetParameterByName`, and passes
the correct header version to `FMOD_Studio_System_Create`. A `.config` file next
to the game's `.exe` maps the DLL names onto the real libraries and redirects a
few renamed calls:

```xml
<configuration>
  <dllmap dll="fmod" os="linux" target="libfmod.so.13"/>
  <dllmap dll="fmodstudio" os="linux" target="libfmodstudio.so.13">
    <dllentry dll="fmodstudio_fix.so" name="FMOD_Studio_EventInstance_SetParameterValue" target="_FMOD_Studio_EventInstance_SetParameterValue"/>
    <dllentry dll="fmodstudio_fix.so" name="FMOD_Studio_System_Create" target="_FMOD_Studio_System_Create"/>
    <dllentry dll="fmodstudio.so.13" name="FMOD_Studio_System_GetLowLevelSystem" target="FMOD_Studio_System_GetCoreSystem"/>
    <dllentry dll="fmodstudio.so.13" name="FMOD_Studio_EventInstance_TriggerCue" target="FMOD_Studio_EventInstance_KeyOff"/>
  </dllmap>
</configuration>
```

This is the Linux half of the `Celeste.exe.config` the port ships. The game reads
it from beside its `.exe`, so the launch script copies it into `gamedata/`.

`fmodstudio_fix.c` hard-codes `FMOD_VERSION`, and it has to match the 2.x
libraries you ship. If `System_Create` fails, that number is the first thing to
check. FMOD also needs an output plugin so it can reach the device's audio. The
Celeste port ships `libfmod_SDL.so`, an FMOD output plugin that goes through SDL,
so it has to be built against the SDL the CFW provides.

*FMODex 4.x (older games).* Games from the FMODex era link `libfmodex.so`, which
doesn't exist on ARM. `fakemodex` exports that legacy ABI and translates the
calls at runtime, through `dlopen`, into whatever real `libfmod.so` is installed.
It currently targets FMOD Core 2.02.05. Its history mentions Bastion and The Swapper. Its own
README is clear about its limits: many functions are ignored, and it works for the
games that were tried and no more. It's a workaround, not a general solution.

**Steam and Epic.** DRM-free games still link to the Steam or Epic Online
Services client libraries, and crash when they're missing. FNAPatches builds
zero-stubs that make every call do nothing:

| Stub | Replaces |
|---|---|
| `libsteam_api.so` (copied also as `libsteam_api64.so`, `CSteamworks` and `libSteamWrapper.so`) | The Steam client API |
| `EOSSDK-Win64-Shipping.so` | Epic Online Services |

Ports ship the one the game asks for in `libs/`. Where a game uses a managed
wrapper instead, such as `Steamworks.NET`, a pure-managed replacement can stand
in for it. OneShot's patches ship one, which removes the native Steam dependency
entirely. The same idea covers other Windows-only assemblies: Blossom Tales
replaces `SlimDX.DirectInput`, whose real build can't load under Mono, with a
managed stub that reports no devices. That's safe there because the game's
gamepad input goes through XNA's `GamePad` instead.

## Textures, memory and ASTC

Desktop games ship textures as DXT (S3TC). When the GPU driver doesn't report
S3TC support, FNA decodes them on the CPU at load time. `Texture2DReader` asks
FNA3D whether the driver supports DXT1 (for DXT1 textures) or S3TC (for DXT3 and
DXT5), and if not, runs the data through `DxtUtil` into full RGBA. That's four
bytes per texel in memory where DXT5 used one, and the decode costs time on every
load.

**ASTC** is the fix: the texture stays compressed on the GPU. Stock FNA has no
ASTC support, so this needs **custom FNA and FNA3D builds**. They add new
`SurfaceFormat` values, `Astc4x4EXT`, `Astc5x5EXT`, `Astc6x6EXT` and
`Astc8x8EXT` plus an `R8` format, and FNA3D's OpenGL driver maps them to
`GL_COMPRESSED_RGBA_ASTC_*_KHR`. The GPU and driver must support ASTC. The
builds are a prerequisite: a port that uses ASTC ships the custom `FNA.dll` and
`libFNA3D`, and the game's textures have to be converted to match.

Bigger blocks mean smaller textures and lower quality:

| Block | Bytes per texel |
|---|---|
| 4x4 | 1.0 |
| 5x5 | 0.64 |
| 6x6 | 0.44 |
| 8x8 | 0.25 |

For comparison, DXT5 is 1.0, so even 4x4 isn't a loss against it, and anything
larger saves memory outright.

**FNARepacker** does the conversion. It's a Mono tool that a patch script runs
once, on the device, against the game's `Content` folder:

```bash
export ASTC_QUALITY=60.0
mono "$GAMEDIR/tools/FNARepacker.exe" "$GAMEDIR/gamedata/Content/GameSpritesheets"
```

It chooses a block size per texture from its size, with larger textures taking
larger blocks:

| Texture area | Block |
|---|---|
| 2048x2048 or more | 8x8 |
| 1024x1024 or more | 6x6 |
| 256x256 or more | 5x5 |
| anything smaller | 4x4 |

Small textures are UI, icons and glyph sheets, where block artifacts show most and
the saving is trivial. Big ones are atlases drawn well below 1:1 on a handheld
screen. 8x8 is not a safe default for hand-painted 2D art with hard alpha edges,
which is exactly what large blocks handle worst. On a real Bastion atlas, 8x8
against 6x6 measured 35.2 dB and looked the same at that scale.

Settings are environment variables:

| Variable | Meaning |
|---|---|
| `ASTC_QUALITY` | The encoder's quality setting. Defaults to medium. Rogue Legacy sets `60.0`. |
| `ASTC_BLOCK` | Forces one block size for every texture: `4x4`, `5x5`, `6x6` or `8x8`. |
| `ASTC_THREADS` | Number of encoder threads. |

Encoding is the slow part of first-time setup. `--guide-out <dir>` encodes
normally and writes guide files recording the encoder's block decisions, and
`--guide-in <dir>` reuses them to skip the search. That lets you do the full
search once on a PC and ship the guides so the device only pays for the quick
pass. `--census <dir>` reports a game's texture formats without changing
anything, which is the first thing to run on a new game.

Celeste does the same job with its own repacker, `celeste-repacker`, which
converts to ASTC 4x4. Its script runs it behind a progress screen, and checks for
a `.astc_done` marker so it only happens once.

Audio can be a memory problem too. Rogue Legacy's patch script also shrinks its
sound effects bank to 44.1 kHz with `xwbshrink.exe`. It keeps the `.bak` backup
until the tool reports success. Blossom Tales has a 302 MB uncompressed wave bank
that FNA's normal `WaveBank` constructor reads into memory whole. Streaming it
instead is a patch, see below.

## Ahead-of-time compilation

Mono compiles code as it runs, which costs startup time and CPU on a slow device.
Ports can precompile the managed assemblies. The `.dll.so` files next to
`FNA.dll` and `SDL2-CS.dll` are Mono AOT images, and Mono uses them
automatically when they sit beside the assembly.

A port can also do it on the device, in a patch script. Rogue Legacy does it for
each of the game's assemblies, skipping any that already have a `.so`:

```bash
mono --aot=full,verbose,print-skipped-methods "$ASMPATH"
```

That produces `Game.dll.so`. AOT needs an assembler and linker, and PortMaster's
Mono runtime bundles them. Its `lib/` folder holds the `libopcodes` and `libbfd`
they depend on, and that folder isn't on `LD_LIBRARY_PATH` by default, so add it,
as the launch script above does:

```bash
export LD_LIBRARY_PATH="$GAMEDIR/libs:$monodir/lib:$LD_LIBRARY_PATH"
```

Mono's other speed flags appear in scripts too. Bleed starts the game with
`mono --ffast-math -O=all`, which turns on all optimizations and fast
floating-point math.

## Patching with MonoMod

Plenty of games need their own code changed: a crash on startup, a window larger
than the screen, a per-frame cost that a handheld can't pay. The method this
guide uses is **MonoMod**, which rewrites a game's assemblies. A patch is a small
C# project that compiles to a `.mm.dll`. It is applied on the device on first
launch, so the port never contains the game's code.

### Applying a patch

A port that patches ships two things: a `monomod/` folder with MonoMod itself
(`MonoMod.exe`, `MonoMod.RuntimeDetour.HookGen.exe` and the libraries they need),
and a `patches/` folder with the compiled patch. Bleed's script runs the whole
sequence:

```bash
export MONOMOD_MODS="$gamedir/patches"
export MONOMOD_DEPDIRS="${MONO_PATH}":"${gamedir}/monomod"

# Generate the hook assembly from the player's game
mono "$gamedir/monomod/MonoMod.RuntimeDetour.HookGen.exe" "$gamedir/gamedata/Bleed.exe"

# Apply the patches
mono "$gamedir/monomod/MonoMod.exe" "$gamedir/gamedata/Bleed.exe"
```

What each step does:

- **`MONOMOD_MODS`** is the folder of patch assemblies to apply.
  **`MONOMOD_DEPDIRS`** is where MonoMod looks for the other assemblies the game
  and the patches refer to. Use the same folders as `MONO_PATH`, plus `monomod/`.
- **HookGen** reads the game's `.exe` and writes `MMHOOK_Bleed.dll`, a generated
  assembly with an event for every method in the game. Patches that hook methods
  at runtime are compiled against it, so it has to exist before the patch runs.
- **`MonoMod.exe`** applies every patch it finds and writes
  **`MONOMODDED_Bleed.exe`** beside the original. The original is never modified.

The game then runs as the patched file:

```bash
mono --ffast-math -O=all MONOMODDED_Bleed.exe
```

Three things about that:

- **Don't redistribute the output.** `MONOMODDED_*.exe` and `MMHOOK_*.dll` are
  derived from the player's game. Ship the tools and the patch, and produce both
  on the device.
- **The save path changes.** Many games derive their save folder from the
  assembly name, and the patched one is called `MONOMODDED_Bleed`. Bleed's script
  binds `~/.local/share/MONOMODDED_Bleed` to the port's `savedata/`. Check where
  the patched game actually writes.
- **Re-patch when anything changes.** Bleed records a SHA-1 of the game and of
  every patch DLL in `.ver_checksum`, and runs `sha1sum -c` on each launch. When
  the game or a patch has changed it deletes the `.patch_done` marker and patches
  again, so updating a patch on the next PortMaster release takes effect without
  the player doing anything.

```bash
sha1sum -c "$gamedir/gamedata/.ver_checksum"
if [ $? -ne 0 ]; then
    rm -f "$gamedir/gamedata/.patch_done"
fi

if [[ ! -f "$gamedir/gamedata/.patch_done" ]]; then
    # ... HookGen and MonoMod.exe, as above ...
    touch "$gamedir/gamedata/.patch_done"
    sha1sum "$gamedir/gamedata/Bleed.exe" > "$gamedir/gamedata/.ver_checksum"
    sha1sum "$gamedir/patches/"*.dll >> "$gamedir/gamedata/.ver_checksum"
fi
```

Some games keep their logic in an engine DLL, not the `.exe`. `MMLoader.exe`, from
FNAPatches, runs an assembly in a fresh `AppDomain`, redirects any referenced
assembly that has a `MONOMODDED_` copy beside it, and lets you override the base
directory: `mono MMLoader.exe Game.exe [appBasePath] [-- args]`.

About eight ports, Celeste, Steel Assault and TMNT: Shredder's Revenge among them,
load a patch DLL through an `FNA_PATCH` variable instead and leave the game's
`.exe` untouched. That relies on a custom FNA build and isn't the route described
here.

### Making a patch

Patches live in [FNAPatches](https://github.com/JohnnyonFlame/FNAPatches), one
folder per game. Make one on a PC with Mono, ideally 6.12 to match the device.

**Set up.** The repository's README gives the full steps. In outline, you need
MonoMod (the `net452` build, `22.05.01.01`), Harmony (`2.2.1.0`), an FNA build, the
game's own assemblies copied into `deps/<Game>/`, and VisFree, the compiler
described below. Reading the game's code in ILSpy is how you find what to change.

**Name things the way MonoMod expects.**

- By convention a patch assembly is named `<TargetAssembly>.<Anything>.mm.dll`.
  Bleed's is `Bleed.BleedPatches.mm.dll`, built from `Bleed.BleedPatches.mm.cs`.
- A class named `patch_Foo` patches the game's class `Foo`.
- Inside it, a method declared `extern` and named `orig_Bar` is the *original*
  `Bar`, which MonoMod preserves under that name. Your own `Bar` replaces it.

**Replace or wrap a method.** The simplest patch changes one method and calls the
original for the rest. This one, from the Cosmic Invasion patches, makes a
context switch with an empty name do nothing instead of crashing:

```csharp
namespace Paris.Game
{
    class patch_GameContextManager
    {
        public extern void orig_SwitchToContext(string newContext, bool add);
        public void SwitchToContext(string newContext, bool add)
        {
            if (string.IsNullOrEmpty(newContext))
                return;
            orig_SwitchToContext(newContext, add);
        }
    }
}
```

A patch class can also inherit from the class it patches, to add fields or
override a virtual method, as `patch_CameraBlockTrigger : CameraBlockTrigger` does
in the same project.

**Rewrite a method's body.** When you need to change a few instructions inside a
method without replacing it, hook its IL. Hooks come from the `MMHOOK_` assembly
that HookGen generated, so a patch like this is compiled against it. Bleed
crashed on startup on some FNA and SDL2 combinations, because it read the display
size through a graphics device that doesn't exist yet. The patch hooks the
constructor, finds those instructions and swaps them for a query of the default
adapter:

```csharp
class patch_Program
{
    extern static void orig_Main(string[] args);
    private static void Main(string[] args)
    {
        // Register hooks before the game starts, then hand control back
        IL.TimeGuy.Game1.ctor += Hook_Game1_ctor;
        orig_Main(args);
    }

    private static void Hook_Game1_ctor(ILContext il)
    {
        ILCursor c = new ILCursor(il);
        if (c.TryGotoNext(MoveType.Before,
            i => i.MatchLdarg(0),
            i => i.MatchLdfld(typeof(TimeGuy.Game1), "graphics"),
            /* ... the rest of the sequence being replaced ... */
        ))
        {
            c.RemoveRange(10);
            c.Emit(OpCodes.Call, typeof(GraphicsAdapter).GetMethod("get_DefaultAdapter"));
            /* ... emit the replacement ... */
        }
    }
}
```

Match the instruction pattern, don't count offsets, and wrap it in
`if (TryGotoNext(...))`. If the player's build differs from yours, the patch then
skips itself instead of corrupting the method.

**Compile with VisFree.** Patches routinely touch `internal` and `private` code,
and a normal compiler refuses. VisFree, in the FNAPatches repo, is a C# compiler
wrapper that ignores access modifiers:

```bash
VisFree.exe GamePatch.dll Patch01.cs Patch02.cs -- Game.exe Engine.dll
```

Each game folder has a `Makefile.inc` listing its sources and dependencies. Bleed's
names the patch source, the `MMHOOK` assembly, and the references:

```make
SRC := $(MAKECMDGOALS)/Bleed.BleedPatches.mm.cs
ASM := deps/$(MAKECMDGOALS)/MMHOOK_Bleed.dll $(SRC:%.cs=out/%.dll)
DEPS := $(DEPS_FOLDER)/Bleed.exe \
        deps/$(MAKECMDGOALS)/MMHOOK_Bleed.dll \
        deps/Cecil/*.dll \
        deps/FNA/FNA.dll \
        deps/MonoMod/MonoMod.exe \
        deps/MonoMod/MonoMod.Utils.dll
```

Then `make Bleed` generates the hook assembly and compiles the patch into
`out/Bleed/`. Copy the result into the port's `patches/`.

**Read the first-launch output.** MonoMod errors on the device are only visible if
the script logs them. Bleed tees every step into `install_log.txt` and stops with a
clear message if `MonoMod.exe` fails.

### What patches have been needed

These are the real reasons ports in the library are patched, from FNAPatches:

- **Performance**: Blossom Tales and Blossom Tales II (render targets, sprite
  batching, audio streaming, see below), Steel Assault and Panzer Paladin
  (general optimizations for low-power devices), and TMNT: Shredder's Revenge
  (performance settings and an OpenGL deadlock).
- **Startup crashes**: Bleed (the display query above), and Panzer Paladin
  (breakage on non-Steam, newer FNA builds).
- **Screen size**: Chasm (fullscreen logic on very small resolutions), and OneShot
  (it opened a fixed 1280x720 window larger than the display).
- **Missing Windows pieces**: OneShot dropped its only two WinForms and GDI+
  calls so no desktop GUI stack is needed, and fixed an FMOD `System_Create`
  P/Invoke that silently left the game without audio.
- **Linux paths and mods**: TMNT: Shredder's Revenge needed file paths fixed for
  Linux, and a companion mod loads custom sound assets.
- **Missing native libraries**: stubs and managed replacements, as above.

## Performance on a handheld GPU

Blossom Tales: The Sleeping King ran at 15 to 20 fps and now runs at 60 on an
aarch64 handheld. How it got there is the most useful lesson about FNA
performance on these devices.

**The GPU here is tile-based** (a Mali, in the case measured). Each
`SetRenderTarget` forces a pipeline flush and a tile resolve, which is a large
fixed cost per bind no matter how little is drawn. So the number of render-target
switches and draw calls matters more than the number of pixels.

- **Oversized render targets.** The game allocated three 2048x2048 targets and a
  1024x1024 one, but only ever rendered a 1280x720 corner of them, then blitted
  the whole oversized surface to the screen with a null source rectangle. That's
  clearing and resolving about 4.19 million pixels per target per frame to show
  0.92 million. It's a fixed cost, paid the same in the menu and in the middle of
  a dungeon, so framerate stays pinned whatever is on screen while the CPU sits
  idle. That pattern, with idle CPU, is the symptom to look for. The patch
  rewrites the allocations to 1280x720.
- **Don't stop at pixels.** After that fix, per-frame pixel work fell about 3x
  but fps only rose from 17 to 25. The game was no longer fill-bound. What hadn't
  changed was the number of render-target switches. Bypassing a final target that
  was copied 1:1 to the backbuffer removed a bind, a clear, a full-screen blit
  and a tile resolve.
- **Batching.** `SpriteSortMode.Immediate` flushes a draw call per sprite.
  `Deferred` batches while keeping submission order, so the output is identical.
  Only code that calls `EffectPass.Apply()` between `Begin` and `Draw` truly
  needs `Immediate`. The game used it in 15 places and needed it in two.
- **Audio memory.** The 302 MB wave bank was read into memory whole at startup
  by FNA's normal `WaveBank` constructor. Marking it as streaming, a four-byte
  header change, and calling FNA's streaming overload keeps only metadata and
  small caches in memory.

Two habits make this kind of work cheaper. Make the patch skip itself when it
doesn't recognize the code, as with the IL hooks above. And apply each
optimization independently so a regression can be bisected.

## Input and saves

FNA reads gamepads through SDL, and XNA's `GamePad` class sits on top of that, so
games that support controllers need no mapping. Every FNA port runs gptokeyb
with no config, just to be able to kill the process:

```bash
$GPTOKEYB "mono" &
```

A game that only handles the keyboard needs a `.gptk` like any other port. See the
[LÖVE guide](love2d.md#input-and-controls) for the formats, which work the same
way here. The first argument stays `mono`.

**Saves.** FNA games write under `~/.local/share/<GameName>`, which isn't inside
the port. `bind_directories` redirects it into `savedata/`:

```bash
bind_directories ~/.local/share/AxiomVerge "$GAMEDIR/savedata"
```

A few ports set `XDG_DATA_HOME` instead. After MonoMod patching, remember that the
name can change, as covered above. Finding where a game really writes is a matter
of running it once and looking.

A few scripts carry fixes for one firmware. Axiom Verge restores a backed-up
`.asoundrc` on ArkOS and dArkOS, for example, to stop audio breaking on some
devices. Keep that kind of workaround scoped to the firmware that needs it.

## Compatibility

- **aarch64 only.** Mono has no other PortMaster build.
- **.NET Framework games.** Anything built for modern .NET won't run on Mono 6.12.
- **Memory.** Handheld RAM is the usual limit. Big wave banks and uncompressed
  textures are the first things to look at, see above.
- **Windows-only dependencies.** WinForms, GDI+, DirectInput, SlimDX and native
  Windows DLLs need a stub or a patch.
- **Steam and Epic libraries.** Use the stubs above.
- **FMOD.** Identify which generation the game uses before you start.
- **SDL3 builds of FNA.** Use the SDL2 route above, since every CFW ships SDL2.
- **Line endings.** CRLF in the `.sh` gives a black screen and no log.

## Tools

- [ILSpy](https://github.com/icsharpcode/ILSpy) decompiles a game's assemblies so
  you can read what to patch.
- [MonoMod](https://github.com/MonoMod/MonoMod) and
  [Harmony](https://harmony.pardeike.net/) do the patching.
- [FNAPatches](https://github.com/JohnnyonFlame/FNAPatches) has VisFree, MMLoader,
  EVBUnpack, the Steam and EOS stubs, `fmodstudio_fix`, and the existing patches.
- [fakemodex](https://github.com/ptitSeb/fakemodex) is the FMODex wrapper.
- [celeste-repacker](https://github.com/JohnnyonFlame/celeste-repacker) converts
  Celeste's textures to ASTC.
- [astc-encoder](https://github.com/ARM-software/astc-encoder) is the encoder the
  repackers use.
- `evbunpack` extracts Enigma Virtual Box bundles.

## Build, files and licensing

- **Build.** FNA, FNA3D and FAudio are built from source for the target. FNA3D and
  FAudio use CMake and take `-DBUILD_SDL3=OFF` for SDL2. FNA3D and FAudio don't
  accept AI-generated code in contributions, so write any patch you send them
  yourself.
- **Licenses.** Ship a file for every component in the port's `licenses/` folder:
  FNA, Mono, MonoXNA, lzxdecoder, Theorafile, libtheora, libogg and libvorbis, plus
  anything else bundled such as MonoMod, Harmony or a stub library.
- **Don't redistribute** the game's assemblies and content, or anything derived
  from them: `MONOMODDED_*` files, `MMHOOK_*` assemblies, repacked textures and
  extracted bundles. Produce all of it on the device from the player's own copy.

## Example ports

FNA ports in the library, useful to unpack and read:

- [Axiom Verge](../../../../port/?name=axiom.verge), a clean current layout,
  FNA3D and FAudio 22.03
- [Rogue Legacy](../../../../port/?name=roguelegacy), user-supplied content, the
  patcher, ASTC repacking, audio shrinking and on-device AOT
- [Bleed](../../../../port/?name=bleed), the full MonoMod apply sequence, with
  checksum-based re-patching
- [Panzer Paladin](../../../../port/?name=panzerpaladin), also patched with
  MonoMod, for performance and for newer FNA builds
- [Celeste](../../../../port/?name=celeste), ASTC repacking behind a progress
  screen, plus the FMOD 1.x to 2.x bridge. It loads its patch through
  `FNA_PATCH`
- [TMNT: Shredder's Revenge](../../../../port/?name=tmntsr), another
  `FNA_PATCH` port, with performance settings and OpenGL fixes
