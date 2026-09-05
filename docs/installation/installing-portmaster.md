# Installing PortMaster

## Option 1: Already Installed (Check First)

Most custom firmware comes with PortMaster pre-installed.

**Check these locations:**

| Custom Firmware | Menu                       |
|-----------------|----------------------------|
| Majority    	  | Ports Section          	   |
| ArkOS & ROCKNIX | Tools Section       	   |
| MuOS	     	  | Application Section        |

**Found it?** You're done! Skip to [Using PortMaster](#using-portmaster).

!!! note "KNULLI Users"
    Go to Ports → "Install PortMaster" and run the script once.

---

## Option 2: Manual Installation

!!! abstract "What you need"
    - SD card reader
    - Access to your device's SD card

[:material-download: Download Install.PortMaster.sh](https://github.com/PortsMaster/PortMaster-GUI/releases){ .md-button .md-button--primary }

### Installation Paths

Place the file in the correct folder:

| Custom Firmware | Folder                     |
|-----------------|----------------------------|
| AmberELEC       | `/roms/ports/`             |
| ArkOS           | `/roms2/ports/`            |
| ROCKNIX         | `/roms/ports/`             |
| muOS            | `/mnt/mmc/ROMS/Ports/`     |
| KNULLI          | `/userdata/roms/ports/`    |
| UnofficialOS    | `/roms/ports/`             |

### Installation Steps

1. Eject SD card from computer
2. Insert into device
3. Navigate to Ports
4. Run "Install PortMaster"

PortMaster is now in your Ports section.

---

## Using PortMaster

!!! warning "Internet Required"
    WiFi connection IS needed to download ports.

### Main Menu

Featured Ports
:   Recommended games from the PortMaster team

All Ports
:   {{ total_port_count }}+ available ports for your device

Ready to Run
:   Free games that don't need commercial files

Manage Ports
:   Reinstall or uninstall existing ports

Options
:   Settings and runtime manager

---

## Offline Setup

!!! info "No WiFi?"
    Install runtimes separately using the [Runtimes Guide](runtimes.md).

---

## Community guides

[Retro Game Corps](https://retrogamecorps.com/) has covered PortMaster in depth.
Worth a look if you'd rather follow along with someone than read reference docs.

- [PortMaster Starter Guide](https://retrogamecorps.com/2024/07/12/portmaster-starter-guide/) (article, July 2024)
- [PortMaster Guide: 500+ PC Games on Handhelds!](https://www.youtube.com/watch?v=1rAe9P74BLI) (video walkthrough)
- [My Favorite PC Ports on Retro Handhelds](https://www.youtube.com/watch?v=4FOlGX499pU) (video, a tour of what the library has)

These are made by the community, not the PortMaster team, and PortMaster has
changed since they were published. The video title says 500+ games, for example,
and the library is past {{ total_port_count }} now. Where they disagree with this
wiki, the wiki is current.
