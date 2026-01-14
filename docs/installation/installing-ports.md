# Installing Ports

## Option 1: Online Installation (Recommended)

!!! abstract "What you need"
    - WiFi connection

### Steps

1. Open PortMaster from Ports section
2. Browse and select a port
3. Press Install
4. Exit PortMaster

The port appears in your Ports section. If not, restart your device.

---

## Option 2: Offline Installation

!!! abstract "What you need"
    - Computer with internet
    - SD card reader

### Step 1: Download Port

1. Go to [portmaster.games/games.html](https://portmaster.games/games.html)
2. Find your port and download the `.zip` file
3. **Don't extract it**

### Step 2: Copy to Autoinstall Folder

| Custom Firmware | Autoinstall Folder                      |
|-----------------|-----------------------------------------|
| AmberELEC       | `/roms/ports/autoinstall/`              |
| ArkOS           | `/roms/ports/autoinstall/`              |
| ROCKNIX         | `/roms/ports/autoinstall/`              |
| muOS            | `/mnt/mmc/ports/autoinstall/` or `/mnt/sdcard/ports/autoinstall/` |
| KNULLI          | `/userdata/roms/ports/autoinstall/`     |

### Step 3: Install

1. Eject SD card from computer
2. Insert into device
3. Launch PortMaster

The port installs automatically.

!!! info "Offline Devices"
    Pre-install runtimes using the [Runtimes Guide](runtimes.md).

---

## Port Types

Ready to Run
:   Free ports that work immediately. No extra files needed.

Commercial Ports
:   Require you to own the game. Additional setup needed after installation.

### Adding Commercial Game Files

After installing a commercial port:

1. Go to the [Games Page](/games).
2. Find your game → Details
3. Follow file placement instructions

---
## Troubleshooting

**Port doesn't appear:**

- Restart device or refresh games list

**Port doesn't run:**

- Check Details page for correct file placement
- Install runtimes via Options → Runtime Manager
- Check the log.txt file for more info

**Autoinstall failedL:**

- Verify `.zip` is not extracted and is in correct folder