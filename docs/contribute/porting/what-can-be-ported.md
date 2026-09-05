# What Can Be Ported?

A game is portable if its code can be made to run on ARM Linux. In practice
that happens one of three ways:

**Native build.** The game is open source, or the developer ships an ARM Linux
build, so it compiles and runs directly. A large share of the library works this
way.

**Engine runtime.** The game's engine has been reimplemented or rebuilt for ARM,
so the original game data runs unmodified on top of it. Godot, Solarus and
RealLive ports all work like this.

**Bytecode VM.** The game isn't native code at all, it's bytecode for a virtual
machine that already runs on ARM. GameMaker, Mono/C#, .NET and Java games fall
here, and the port supplies the VM. This is the biggest group, mostly because of
GameMaker.

If none of those apply, the game generally can't be ported. The usual blockers
are a closed-source engine with no ARM target, and anti-cheat or DRM that expects
an x86 Windows environment.

!!! tip
    [:simple-steamdb: SteamDB](https://steamdb.info/) is the quickest way to
    find out what engine and technologies a commercial game uses before you
    invest any time in it.

## Engines and frameworks

These are the engines and frameworks known to work, ordered roughly by how
common they are in the library. The order is a fair guide to how well-travelled
each route is, which usually tracks how much help you'll find if you get stuck.

| Engine / framework | How it runs | Template | Guide |
|---|---|---|---|
| **GameMaker** | GMLoader / GMLoaderNext runs the game's `data.win` | [GameMaker](script-templates.md) | [Guide](engines/gamemaker-studio.md) |
| **Godot** | Godot 3 via FRT, Godot 4 via a Godot runtime | [Godot 3, Godot 4](script-templates.md) | [Guide](engines/godot.md) |
| **Love2D** | LÖVE binary runs the `.love` file | [Love2d](script-templates.md) | [Guide](engines/love2d.md) |
| **Mono / C#** | Mono runtime executes the game's assemblies | — | *needed* |
| **Python / pygame** | Python interpreter plus the game's modules | — | *needed* |
| **.NET** | .NET runtime | — | *needed* |
| **Pyxel** | Pyxel runtime (Python) | [Pyxel](script-templates.md) | *needed* |
| **Ren'Py** | Ren'Py runtime (Python) | — | *needed* |
| **AGS** | Adventure Game Studio engine build | — | *needed* |
| **Java / libGDX** | JDK/JRE runtime | [Java, LibGDX](script-templates.md) | *needed* |
| **RealLive** | `rlvm` engine reimplementation | — | *needed* |
| **Solarus** | Solarus engine build | — | *needed* |

GameMaker is by far the largest group, and most of those ports now use
GMLoaderNext rather than the original GMLoader.

### Native builds are the other half

A large share of the library matches none of the rows above, because those ports
don't sit on a shared engine at all: they're native ARM builds that ship their
own binary, mostly SDL-based C and C++ games.

A small number take a different route again and run an x86 binary through
`box86`/`box64` translation. It works, but it costs performance, so it's a last
resort rather than a starting point.

!!! warning
    This is a guide to feasibility, not a guarantee. A game using a supported
    engine can still be blocked by DRM, native plugins, an unusual build, or
    performance that simply won't hold up on handheld hardware.
