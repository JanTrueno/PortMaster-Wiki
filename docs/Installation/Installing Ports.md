# Installing Ports

PortMaster is a simple GUI tool designed to download and install game ports for Linux handheld devices. Here's how you can install ports using PortMaster:

## Best Experience: Using PortMaster Application

For the best experience, you should download and install ports through the PortMaster Application. This ensures that the installed port has the correct permissions and metadata.

### Installation Process

1. **Open PortMaster Application**
2. **Browse the available ports** and select the one you want to install.
3. **Install the port** – PortMaster handles all the details and ensures everything is set up correctly for your device.

## Offline Installation

If your device doesn’t have Wi-Fi or you can’t use the PortMaster app, follow these steps for offline installation:

### 1. Download the Port

Go to the [PortMaster repository](https://portmaster.games/games.html) and find the port you want to install. Download the `.zip` file for the desired port.

### 2. Place the Port in the Autoinstall Folder

Copy the downloaded `.zip` file into the appropriate autoinstall folder for your device:

- **AmberELEC, ROCKNIX, uOS, Jelos:** `/roms/ports/PortMaster/autoinstall/`
- **muOS:** `/mmc/MUOS/PortMaster/autoinstall/`
- **ArkOS:** `/roms/tools/PortMaster/autoinstall/`
- **Knulli:** `/userdata/system/.local/share/PortMaster/autoinstall/`

### 3. Run the PortMaster Application

Launch the PortMaster Application. The port will be installed automatically.

## Alternative: Manual Installation (Not Recommended)

If the autoinstall folder method doesn't work, you can unzip the contents of the port into the corresponding ports folder for each custom firmware (CFW). However, this may break the port, and it may no longer start properly.

Here are the port folder locations for manual installation:

- **AmberELEC, ROCKNIX, uOS, Jelos:** `/roms/ports/`
- **muOS:** `/mmc/ports/` (for the folders) or `/mnt/mmc/ROMS/Ports/` (for the `.sh` files)
- **ArkOS:** `/roms/tools/PortMaster/autoinstall/`
- **Knulli:** `/userdata/system/.local/share/PortMaster/autoinstall/`

