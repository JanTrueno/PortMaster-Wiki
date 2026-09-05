# Packaging Ports for PortMaster

To release a port on PortMaster there are some guidelines that need to be
followed.

## Port structure

Ports live in the `ports` top level directory, each in its own sub-directory
named after the port. Every port needs a `port.json`, a `screenshot.{jpg,png}`,
a `README.md`, a `gameinfo.xml`, a launch script and a port directory. A
`cover.{jpg,png}` is optional.

The launch script can have capital letters and spaces, like `Port Name.sh`, and
must end in `.sh`. The port directory must match the name of the directory
containing it. Some legacy ports break these rules, but new ports are not
accepted unless they follow the current convention.

Script names and port directories must be unique across the whole project.
Checks run on submission to make sure of it.

```
portname/
├── port.json
├── README.md
├── screenshot.jpg
├── gameinfo.xml
├── cover.jpg (optional)
├── Port Name.sh
└── portname/
    ├── licenses/
    │   └── LICENSE files
    └── <port files here>
```

The **portname** itself has its own rules:

- It must start with a lowercase letter (a-z) or a number (0-9).
- After that you can use lowercase letters (a-z), numbers (0-9), periods (.)
  or underscores (\_).
- There is no length limit, but keep it short.
- It must not clash with any existing port.

## port.json

This is what PortMaster itself reads, and it holds all the pertinent info for
the port. The [JSON Generator](../../tools/json-generator.md) will build one for
you.

Make sure to select the correct architecture. If the game uses a runtime such as
Godot, Mono or Java, no arch needs to be entered.

Example, from 2048:

```json
{
    "version": 2,
    "name": "2048.zip",
    "items": [
        "2048.sh",
        "2048"
    ],
    "items_opt": null,
    "attr": {
        "title": "2048",
        "desc": "The 2048 puzzle game",
        "inst": "Ready to run.",
        "genres": [
            "puzzle"
        ],
        "porter": [
            "Christian_Haitian"
        ],
        "image": {},
        "rtr": true,
        "runtime": null,
        "reqs": [],
        "arch": [
            "aarch64",
            "armhf"
        ]
    }
}
```

## README.md

This provides the additional info shown for the port on the wiki. The
[README Generator](../../tools/markdown-generator.md) will build one for you.

Always include a thank you to the developer or creator. Without these people we
would not be here.

Example:

````md
## Notes

Thanks to the [Alien Blaster Team](https://www.schwardtnet.de/alienblaster/) for
creating this game and making it available for free!

## Controls

| Button | Action |
|--|--|
|A| Special Weapon|
|B| Main Weapon|
|X| Swap Weapon|
|Y| Swap Special Weapon |
|R1| Key "1" |

## Compile

```
wget http://www.schwardtnet.de/alienblaster/archives/alienblaster-1.1.0.tgz
cd alienblaster-1.1.0
make
```
````

## screenshot.png

Used in the PortMaster GUI and on the wiki, so it needs to show gameplay or the
port's main function. It has to be exactly 640x480, as either `.jpg` or `.png`.

## gameinfo.xml and cover.png

PortMaster installs metadata, including a cover, into EmulationStation when a
port is installed. That comes from a `gameinfo.xml` and a cover file.

The cover should show gameplay in addition to other media such as box art or a
logo. If no cover is supplied, PortMaster falls back to the screenshot.

The [Gameinfo Generator](../../tools/gameinfo-generator.md) creates and edits
`gameinfo.xml`, and the [Cover Generator](../../tools/cover-generator.md) builds
a `cover.png` from your artwork.

A filled out `gameinfo.xml` looks like this:

```xml
<?xml version="1.0" encoding="utf-8"?>
<gameList>
  <game>
    <path>./Angband.sh</path>
    <name>Angband</name>
    <desc>Angband is a free, single-player dungeon exploration game.

You play an adventurer seeking riches, fighting monsters, and preparing for a final battle with Morgoth, the Lord of Darkness.</desc>
    <releasedate>20230819T000000</releasedate>
    <developer>Angband Development Team</developer>
    <publisher>Angband Development Team</publisher>
    <genre>RPG</genre>
    <image>./angband/cover.png</image>
  </game>
</gameList>
```

## Licenses

Add license files for all sources, libraries and assets you used, in a
`licenses` subfolder. For example:

- The game project's own license, if it's an open source game
- gptokeyb
- sdl1.2 compat
- gl4es
- box86 / box64
- any `.so` libraries you shipped

You can usually find these either in the source folder you compiled from, or on
your build system under `/usr/share/doc/<package>/copyright`.

## The launch script

!!! info inline end "Example scripts"
    Ready-made scripts for each engine are on the
    [Script Templates](script-templates.md) page.

Below is a launch script with every section annotated, explaining what each part
does.

```bash
#!/bin/bash

# Below we assign the source of the control folder (which is the PortMaster folder) based on the distro:

XDG_DATA_HOME=${XDG_DATA_HOME:-$HOME/.local/share}

if [ -d "/opt/system/Tools/PortMaster/" ]; then
  controlfolder="/opt/system/Tools/PortMaster"
elif [ -d "/opt/tools/PortMaster/" ]; then
  controlfolder="/opt/tools/PortMaster"
elif [ -d "$XDG_DATA_HOME/PortMaster/" ]; then
  controlfolder="$XDG_DATA_HOME/PortMaster"
else
  controlfolder="/roms/ports/PortMaster"
fi

source $controlfolder/control.txt # We source the control.txt file contents here
# The $ESUDO, $directory, $param_device and necessary sdl configuration controller configurations will be sourced from the control.txt file shown [here]

# If a Port is built for armhf architecture only (Need for Speed 2 for example) we set this flag so that some environment condition variables are set in the CFWs mod files.
# Example "https://github.com/PortsMaster/PortMaster-GUI/blob/main/PortMaster/mod_JELOS.txt"
export PORT_32BIT="Y" # If using a 32 bit port, else comment it out.

# We source custom mod files from the portmaster folder example mod_jelos.txt which containts pipewire fixes
[ -f "${controlfolder}/mod_${CFW_NAME}.txt" ] && source "${controlfolder}/mod_${CFW_NAME}.txt"

# We pull the controller configs like the correct SDL2 Gamecontrollerdb GUID from the get_controls function from the control.txt file here
get_controls

# We switch to the port's directory location below & set the variable for the gamedir and a configuration dir  easier handling below
GAMEDIR=/$directory/ports/portfolder/
CONFDIR="$GAMEDIR/conf/"

# Ensure the conf directory exists
mkdir -p "$GAMEDIR/conf"

# Switch to the game directory
cd $GAMEDIR

# Log the execution of the script, the script overwrites itself on each launch
> "$GAMEDIR/log.txt" && exec > >(tee "$GAMEDIR/log.txt") 2>&1

# Some ports like to create save files or settings files in the user's home folder or other locations. We map these config folders so we can either preconfigure games and or have the savefiles in one place.
# You can either use XDG variables to redirect the Ports to our gamefolder if the port supports it:

# Set the XDG environment variables for config & savefiles
export XDG_DATA_HOME="$CONFDIR"

# OR

# Use bind_directories to reroute that to a location within the ports folder.
bind_directories ~/.portfolder $GAMEDIR/conf/.portfolder

# Port specific additional libraries should be included within the port's directory in a separate subfolder named libs.aarch64, libs.armhf or libs.x64
export LD_LIBRARY_PATH="$GAMEDIR/libs.${DEVICE_ARCH}:$LD_LIBRARY_PATH"

# Provide appropriate controller configuration if it recognizes SDL controller input
export SDL_GAMECONTROLLERCONFIG="$sdl_controllerconfig"

# If a port uses GL4ES (libgl.so.1) a folder named gl4es.aarch64 etc. needs to be created with the libgl.so.1 file in it. This makes sure that each cfw and device get the correct GL4ES export.
if [ -f "${controlfolder}/libgl_${CFW_NAME}.txt" ]; then
  source "${controlfolder}/libgl_${CFW_NAME}.txt"
else
  source "${controlfolder}/libgl_default.txt"
fi

# We launch gptokeyb using this $GPTOKEYB variable as it will take care of sourcing the executable from the central location,
# assign the appropriate exit hotkey dependent on the device (ex. select + start for most devices and minus + start for the
# rgb10) and assign the appropriate method for killing an executable dependent on the OS the port is run from.
# With -c we assign a custom mapping file else gptokeyb will only run as a tool to kill the process.
# For $ANALOG_STICKS we have the ability to supply multiple gptk files to support 1 and 2 analogue stick devices in different ways.
# For a proper documentation how gptokeyb works: [Link](https://github.com/PortsMaster/gptokeyb)
$GPTOKEYB "portexecutable.${DEVICE_ARCH}" -c "./portname.gptk.$ANALOG_STICKS" &

# Do some platform specific stuff right before the port is launched but after GPTOKEYB is run.
pm_platform_helper "$GAMEDIR/portexecutable.${DEVICE_ARCH}"

# Now we launch the port's executable with multiarch support. Make sure to rename your file according to the architecture you built for. E.g. portexecutable.aarch64
./portexecutable.${DEVICE_ARCH}

# Cleanup any running gptokeyb instances, and any platform specific stuff.
pm_finish
```

## Functions and error handling

Some games need installation or patching on first run. Use functions to keep the
launch script organised, and error handling inside them to keep it stable.

```bash
# Functions
install() {
    pm_message "Performing first-run setup..."
    # Purge unneeded files
    rm -rf assets/*.exe assets/*.dll assets/.gitkeep
    # Rename data.win
    pm_message "Moving game files..."
    mv "./assets/data.win" "./game.droid" || return 1
    mv assets/* ./
    rmdir assets
    # Do localization fonts and xdelta patch if low ram
    if [ $DEVICE_RAM -lt 2 ]; then
        rm -rf "$GAMEDIR/localization_fonts.csv"
        mv patch/localization_fonts.csv ./
        find $GAMEDIR -type f -iname "*.ttf" ! -iname "Commodore Rounded v1-1.ttf" ! -iname "small_pixel.ttf" -delete
        apply_patch && rm -rf "$GAMEDIR/patch" # Only remove if function is successful
    fi
}

apply_patch() {
    pm_message "Applying patch..."
    if [ -f "$controlfolder/xdelta3" ]; then
        error=$("$controlfolder/xdelta3" -d -s "$GAMEDIR/game.droid" "$GAMEDIR/patch/iosas.xdelta" "$GAMEDIR/game2.droid" 2>&1)
        if [ $? -eq 0 ]; then
            rm -rf "$GAMEDIR/game.droid"
            mv "$GAMEDIR/game2.droid" "$GAMEDIR/game.droid"
            pm_message "Patch applied successfully."
        else
            pm_message "Failed to apply patch. Error: $error"
            rm -f "$GAMEDIR/game2.droid"
            return 1
        fi
    else
        pm_message "Error: xdelta3 not found in $controlfolder. Try updating PortMaster."
        return 1
    fi
}

if [ ! -f "$GAMEDIR/game.droid" ] && [ ! -f "$GAMEDIR/.installed" ]; then
    install && touch "$GAMEDIR/.installed" # Only touch if function is successful
fi
```

Several things to note here:

- The line moving `game.droid` returns `1` immediately if it fails, which stops
  the install function proceeding after a critical task didn't complete.
- `apply_patch` and the `.csv` file are only used if the device has less than
  2GB of RAM, using the `$DEVICE_RAM` variable filled by `control.txt`.
- The `$GAMEDIR/patch` directory is only removed if `apply_patch` succeeded,
  via `&&`. That lets the user correct mistakes during install without
  reinstalling the port.
- `apply_patch` is a nest of conditionals for error checking, and returns `1` if
  it failed.
- `install` only runs once. On success a `.installed` file is created, which
  prevents it running again.
