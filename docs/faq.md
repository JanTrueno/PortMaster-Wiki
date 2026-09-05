# Frequently Asked Questions

## Getting started

### What is PortMaster?

A free, open-source tool for installing game ports on Linux-based handhelds. It
handles downloading, installing, updating and removing ports so you don't have to
copy files around by hand.

It runs on custom firmware such as ROCKNIX, ArkOS, muOS, KNULLI, AmberELEC and
UnofficialOS. Stock firmware is generally not supported. The full list is on
[Supported Handhelds](installation/supported-handhelds.md), and
[Installing PortMaster](installation/installing-portmaster.md) covers setup.

### Do I need WiFi?

To install ports from inside PortMaster, yes. Without WiFi you can still install
ports by downloading the `.zip` on a computer and dropping it into the
`autoinstall` folder on your SD card. See
[Installing Ports](installation/installing-ports.md#option-2-offline-installation)
for the folder path for your firmware.

Runtimes can be pre-installed the same way, which matters if the device will
never be online. See the [Runtimes Guide](installation/runtimes.md).

---

## Ready to Run, and games you supply

Ports come in two kinds, and the difference decides whether you need to do
anything after installing.

**Ready to Run** ports install and play immediately. These are open-source games,
freeware with the right licensing, or games where the developer gave permission
to distribute. Nothing else is needed. They're marked **RTR** on the games list.

**Everything else** requires you to already own the game and supply its files
yourself. PortMaster installs the port, you provide the game.

We don't distribute copyrighted game files and we don't support piracy. Buy the
game from a legitimate source (Steam, GOG, Epic, itch.io) and use those files.
Pre-packaged ports that bundle commercial game files without permission aren't
welcome here.

PortMaster itself is legal, open-source software: it installs ports using games
you already own, and ships no copyrighted content. Licence details are in the
[GitHub repositories](https://github.com/PortsMaster).

---

## Adding your own game files

This is the step most people get stuck on.

1. Install the port from PortMaster first. This creates the port's folder and
   tells you what it expects.
2. Find the game on the [games list](games.md#browse) and open its page. Each
   port's instructions say exactly which files it wants and where they go.
3. Copy the files from your own copy of the game onto the SD card, into the
   port's folder.

The port's folder lives inside the ports directory for your firmware:

| Custom Firmware | Ports folder            |
|-----------------|-------------------------|
| AmberELEC       | `/roms/ports/`          |
| ArkOS           | `/roms2/ports/`         |
| ROCKNIX         | `/roms/ports/`          |
| muOS            | `/mnt/mmc/ROMS/Ports/`  |
| KNULLI          | `/userdata/roms/ports/` |
| UnofficialOS    | `/roms/ports/`          |

### It still says files are missing

Usually one of these:

- **The files are one folder too deep.** Copying a folder out of a zip often
  gives you `gamedata/gamedata/…`. The port expects the files themselves, not a
  folder containing them.
- **Wrong version of the game.** Ports are usually built against a specific
  release. A different store version, a different language build, or a newer
  patch can ship different filenames.
- **Case matters.** `Data.win` and `data.win` are different files on the device
  even if they weren't on your PC.
- **The port wants specific files, not everything.** Copying the whole game
  directory when it asked for two files can be as broken as copying nothing.

---

## Will it run on my device?

Not every port runs on every handheld. Two things decide it: whether the port
supports your device's architecture and firmware, and whether your hardware meets
the port's requirements.

On the [games list](games.md#browse) you can set your device and operating system
in the filter panel. Ports that won't run are then marked, and **Hide
Incompatible** removes them from the list entirely. Each port's own page also has
a device check that tells you directly whether that port will run on what you've
selected.

Ports list requirements, and these are the ones you'll see most:

| Requirement | Meaning |
|-------------|---------|
| `power`     | Needs a CPU above an RK3326 |
| `opengl`    | Needs real OpenGL, not OpenGL ES |
| `2gb`, `4gb` | Minimum RAM |
| `hires`     | Needs a display above 640x480 |
| `!lowres`   | Won't run at 480x320 (RG351P, OGA, ZPG Pro, RG10) |

If a port needs more than your device has, it isn't a setting you can change.
That port won't run on that hardware.

---

## Saves, updates and removing ports

**Saves** are kept inside the port's own folder, not in a system-wide save
directory. Ports are written to redirect the game's save and config locations
into their own folder, which keeps everything for a game in one place and makes
it easy to back up: copy the port's folder off the SD card.

**Updating a port** keeps your saves, because the save folder isn't touched.
Back up first if a game has a long playthrough in it and you can't easily
replace it.

**Removing a port** is done from **Manage Ports** inside PortMaster. That
uninstalls the port cleanly. If you delete a port's folder by hand instead, you
can leave the games list showing an entry that no longer works.

---

## When something doesn't work

### A port is installed but doesn't appear

Refresh or reload your games list, which works differently on each firmware, and
restart the device if that doesn't do it. Make sure you exited PortMaster
properly rather than pulling power, as the list is updated on exit.

### A port launches then closes immediately

Read `log.txt`. Every port writes one into its own folder, and it's the single
most useful thing you can look at. The last few lines usually name the missing
file or library outright.

Common causes, in the order worth checking:

1. Game files missing or in the wrong place. See
   [Adding your own game files](#adding-your-own-game-files) above.
2. A missing runtime. Install it via **Options → Runtime Manager**, or see the
   [Runtimes Guide](installation/runtimes.md).
3. The port doesn't support your device. See
   [Will it run on my device?](#will-it-run-on-my-device) above.

### No sound, or the display is the wrong size

These are usually port-specific rather than something wrong with your setup.
Check the port's page for known issues, then `log.txt`, then ask on Discord with
the log to hand.

### PortMaster itself won't launch or won't update

Check that you're online, that there's free space on the card, and that your
firmware is up to date. If it's still broken, reinstall using the
[installation guide](installation/installing-portmaster.md). Reinstalling
PortMaster does not remove ports you've already installed.

---

## Still stuck?

Ask on Discord. Bring your device model, your firmware, the port name, and the
contents of the port's `log.txt`, and you'll get an answer much faster.

[:fontawesome-brands-discord: Join Discord](https://discord.gg/eqjK6yNQS4){ .md-button }
