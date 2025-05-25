# Packaging Ports for PortMaster

## Launch Script Templates
!!! info inline end 

    These scripts are for ports that support native rendering to kms/drm, for X11 ports see below!

=== "Basic"

    ``` bash
    #!/bin/bash
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

    source $controlfolder/control.txt
    [ -f "${controlfolder}/mod_${CFW_NAME}.txt" ] && source "${controlfolder}/mod_${CFW_NAME}.txt"

    get_controls
    GAMEDIR=/$directory/ports/portfolder/
    CONFDIR="$GAMEDIR/conf/"

    mkdir -p "$GAMEDIR/conf"
    cd $GAMEDIR

    > "$GAMEDIR/log.txt" && exec > >(tee "$GAMEDIR/log.txt") 2>&1

    export XDG_DATA_HOME="$CONFDIR"
    export LD_LIBRARY_PATH="$GAMEDIR/libs.${DEVICE_ARCH}:$LD_LIBRARY_PATH"
    export SDL_GAMECONTROLLERCONFIG="$sdl_controllerconfig"
    bind_directories ~/.portfolder $GAMEDIR/conf/.portfolder

    $GPTOKEYB "portexecutable.${DEVICE_ARCH}" -c "./portname.gptk.$ANALOGSTICKS" &
    pm_platform_helper "$GAMEDIR/portexecutable.${DEVICE_ARCH}"
    ./portexecutable.${DEVICE_ARCH}
    pm_finish
    ```

=== "Godot 3"

    ``` bash
    #!/bin/bash

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

    source $controlfolder/control.txt

    [ -f "${controlfolder}/mod_${CFW_NAME}.txt" ] && source "${controlfolder}/mod_${CFW_NAME}.txt"

    get_controls

    GAMEDIR=/$directory/ports/portfolder/
    CONFDIR="$GAMEDIR/conf/"

    > "$GAMEDIR/log.txt" && exec > >(tee "$GAMEDIR/log.txt") 2>&1

    mkdir -p "$GAMEDIR/conf"
    cd $GAMEDIR

    runtime="frt_3.2.3"
    if [ ! -f "$controlfolder/libs/${runtime}.squashfs" ]; then
      # Check for runtime if not downloaded via PM
      if [ ! -f "$controlfolder/harbourmaster" ]; then
        pm_message "This port requires the latest PortMaster to run, please go to https://portmaster.games/ for more info."
        sleep 5
        exit 1
      fi

      $ESUDO $controlfolder/harbourmaster --quiet --no-check runtime_check "${runtime}.squashfs"
    fi

    # Set the XDG environment variables for config & savefiles
    export XDG_DATA_HOME="$CONFDIR"
    export SDL_GAMECONTROLLERCONFIG="$sdl_controllerconfig"

    #  If XDG Path does not work
    # Use _directories to reroute that to a location within the ports folder.
    bind_directories ~/.portfolder $GAMEDIR/conf/.portfolder 

    # Setup Godot
    godot_dir="$HOME/godot"
    godot_file="$controlfolder/libs/${runtime}.squashfs"
    $ESUDO mkdir -p "$godot_dir"
    $ESUDO umount "$godot_file" || true
    $ESUDO mount "$godot_file" "$godot_dir"
    PATH="$godot_dir:$PATH"

    # By default FRT sets Select as a Force Quit Hotkey, with this we disable that.
    export FRT_NO_EXIT_SHORTCUTS=FRT_NO_EXIT_SHORTCUTS 


    $GPTOKEYB "$runtime" -c "./godot.gptk" &
    pm_platform_helper "$godot_dir/$runtime"
    "$runtime" $GODOT_OPTS --main-pack "gamename.pck"

    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "$godot_dir"
    fi
    pm_finish
    ```

<br>
!!! info inline end 

    These scripts are for ports that X11 windowing and therefore need the WestonPack runtime!

=== "Basic"

    ``` bash
    #!/bin/bash
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

    source $controlfolder/control.txt
    [ -f "${controlfolder}/mod_${CFW_NAME}.txt" ] && source "${controlfolder}/mod_${CFW_NAME}.txt"

    get_controls
    GAMEDIR=/$directory/ports/portfolder/
    CONFDIR="$GAMEDIR/conf/"

    mkdir -p "$GAMEDIR/conf"
    cd $GAMEDIR

    > "$GAMEDIR/log.txt" && exec > >(tee "$GAMEDIR/log.txt") 2>&1

    export XDG_DATA_HOME="$CONFDIR"
    export LD_LIBRARY_PATH="$GAMEDIR/libs.${DEVICE_ARCH}:$LD_LIBRARY_PATH"
    export SDL_GAMECONTROLLERCONFIG="$sdl_controllerconfig"
    bind_directories ~/.portfolder $GAMEDIR/conf/.portfolder

    $GPTOKEYB "portexecutable.${DEVICE_ARCH}" -c "./portname.gptk.$ANALOGSTICKS" &
    pm_platform_helper "$GAMEDIR/portexecutable.${DEVICE_ARCH}"
    ./portexecutable.${DEVICE_ARCH}
    pm_finish
    ```

=== "Godot 4"

    ``` bash
    #!/bin/bash

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

    source $controlfolder/control.txt

    [ -f "${controlfolder}/mod_${CFW_NAME}.txt" ] && source "${controlfolder}/mod_${CFW_NAME}.txt"

    get_controls

    GAMEDIR=/$directory/ports/portfolder/
    CONFDIR="$GAMEDIR/conf/"

    > "$GAMEDIR/log.txt" && exec > >(tee "$GAMEDIR/log.txt") 2>&1

    mkdir -p "$GAMEDIR/conf"
    cd $GAMEDIR

    runtime="frt_3.2.3"
    if [ ! -f "$controlfolder/libs/${runtime}.squashfs" ]; then
      # Check for runtime if not downloaded via PM
      if [ ! -f "$controlfolder/harbourmaster" ]; then
        pm_message "This port requires the latest PortMaster to run, please go to https://portmaster.games/ for more info."
        sleep 5
        exit 1
      fi

      $ESUDO $controlfolder/harbourmaster --quiet --no-check runtime_check "${runtime}.squashfs"
    fi

    # Set the XDG environment variables for config & savefiles
    export XDG_DATA_HOME="$CONFDIR"
    export SDL_GAMECONTROLLERCONFIG="$sdl_controllerconfig"

    #  If XDG Path does not work
    # Use _directories to reroute that to a location within the ports folder.
    bind_directories ~/.portfolder $GAMEDIR/conf/.portfolder 

    # Setup Godot
    godot_dir="$HOME/godot"
    godot_file="$controlfolder/libs/${runtime}.squashfs"
    $ESUDO mkdir -p "$godot_dir"
    $ESUDO umount "$godot_file" || true
    $ESUDO mount "$godot_file" "$godot_dir"
    PATH="$godot_dir:$PATH"

    # By default FRT sets Select as a Force Quit Hotkey, with this we disable that.
    export FRT_NO_EXIT_SHORTCUTS=FRT_NO_EXIT_SHORTCUTS 


    $GPTOKEYB "$runtime" -c "./godot.gptk" &
    pm_platform_helper "$godot_dir/$runtime"
    "$runtime" $GODOT_OPTS --main-pack "gamename.pck"

    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "$godot_dir"
    fi
    pm_finish
    ```



