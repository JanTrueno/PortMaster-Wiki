# Packaging Ports for PortMaster

## Standard Portscript Templates

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




=== "Love2d"
    ```bash
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

    GAMEDIR=/$directory/ports/portfolder
    CONFDIR="$GAMEDIR/conf/"

    mkdir -p "$GAMEDIR/conf"
    cd $GAMEDIR

    > "$GAMEDIR/log.txt" && exec > >(tee "$GAMEDIR/log.txt") 2>&1

    # Set the XDG environment variables for config & savefiles
    export XDG_DATA_HOME="$CONFDIR"

    #  If XDG Path does not work
    # Use bind_directories to reroute that to a location within the ports folder.
    bind_directories ~/.portfolder $GAMEDIR/conf/.portfolder 

    export LD_LIBRARY_PATH="$GAMEDIR/libs.${DEVICE_ARCH}:$LD_LIBRARY_PATH"
    export SDL_GAMECONTROLLERCONFIG="$sdl_controllerconfig"

    source $controlfolder/runtimes/"love_11.5"/love.txt

    # Run the love runtime
    $GPTOKEYB "$LOVE_GPTK" &
    pm_platform_helper "$LOVE_BINARY"
    $LOVE_RUN "$GAMEDIR/lovegame"

    pm_finish
    ```




=== "GameMaker"
    ```bash
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

    export controlfolder

    source $controlfolder/control.txt

    export PORT_32BIT="Y" # If using a 32 bit port
    [ -f "${controlfolder}/mod_${CFW_NAME}.txt" ] && source "${controlfolder}/mod_${CFW_NAME}.txt"

    get_controls

    GAMEDIR=/$directory/ports/portfolder/

    cd $GAMEDIR
    > "$GAMEDIR/log.txt" && exec > >(tee "$GAMEDIR/log.txt") 2>&1

    export LD_LIBRARY_PATH="$GAMEDIR/libs.${DEVICE_ARCH}:$LD_LIBRARY_PATH"
    export GMLOADER_DEPTH_DISABLE=1
    export GMLOADER_SAVEDIR="$GAMEDIR/gamedata/"
    export GMLOADER_PLATFORM="os_linux"
    export SDL_GAMECONTROLLERCONFIG="$sdl_controllerconfig"
    $ESUDO chmod +x "$GAMEDIR/gmloader"

    # if no .gptk file is used use $GPTOKEYB "gmloader" & 
    $GPTOKEYB "gmloader" -c ./controls.gptk &
    pm_platform_helper "gmloader"
    ./gmloader donor.apk

    pm_finish
    ```




=== "Pyxel"
    ```bash
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
    CONFDIR="$GAMEDIR/conf"
    PYXEL_PKG="gamename.pyxapp"

    cd "${GAMEDIR}"

    > "${GAMEDIR}/log.txt" && exec > >(tee "${GAMEDIR}/log.txt") 2>&1

    mkdir -p "$GAMEDIR/conf"
    bind_directories "$HOME/.config/.pyxel/gamename" "$CONFDIR"
    # note: replace gamename with the appropriate value for the game

    # Load Pyxel runtime
    runtime="pyxel_2.2.8_python_3.11"
    export pyxel_dir="$HOME/pyxel"
    mkdir -p "${pyxel_dir}"

    if [ ! -f "$controlfolder/libs/${runtime}.squashfs" ]; then
      # Check for runtime if not downloaded via PM
      if [ ! -f "$controlfolder/harbourmaster" ]; then
        pm_message "This port requires the latest PortMaster to run, please go to https://portmaster.games/ for more info."
        sleep 5
        exit 1
      fi

      $ESUDO $controlfolder/harbourmaster --quiet --no-check runtime_check "${runtime}.squashfs"
    fi

    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${pyxel_dir}"
    fi

    $ESUDO mount "$controlfolder/libs/${runtime}.squashfs" "${pyxel_dir}"

    export SDL_GAMECONTROLLERCONFIG="$sdl_controllerconfig"

    $GPTOKEYB "pyxel" &

    pm_platform_helper "${pyxel_dir}/bin/pyxel"

    # Enable Pyxel virtual env
    source "${pyxel_dir}/bin/activate"
    export PYTHONHOME="${pyxel_dir}"
    export PYTHONPYCACHEPREFIX="${GAMEDIR}/${runtime}.cache"

    # play the pyxel package stored in gamedata
    "${pyxel_dir}/bin/pyxel" play "${GAMEDIR}/gamedata/${PYXEL_PKG}"

    # Alternatively, run a python script file
    # "${pyxel_dir}/bin/pyxel" run gamedata/main.py

    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${pyxel_dir}"
    fi

    pm_finish
    ```




<br>

--- 

## Westonpack Portscript Templates


=== "Godot 4"

    ``` bash
    #!/bin/bash

    # PortMaster preamble
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

    # Adjust these to your paths and desired godot version
    GAMEDIR=/$directory/ports/your_port_folder
    godot_runtime="godot_4.2.2"
    godot_executable="godot422.$DEVICE_ARCH"
    pck_filename="YourGame.pck"
    gptk_filename="YourControls.gptk"

    # Logging
    > "$GAMEDIR/log.txt" && exec > >(tee "$GAMEDIR/log.txt") 2>&1

    # Create directory for save files
    CONFDIR="$GAMEDIR/conf/"
    $ESUDO mkdir -p "${CONFDIR}"

    # Mount Weston runtime
    weston_dir=/tmp/weston
    $ESUDO mkdir -p "${weston_dir}"
    weston_runtime="weston_pkg_0.2"
    if [ ! -f "$controlfolder/libs/${weston_runtime}.squashfs" ]; then
      if [ ! -f "$controlfolder/harbourmaster" ]; then
        pm_message "This port requires the latest PortMaster to run, please go to https://portmaster.games/ for more info."
        sleep 5
        exit 1
      fi
      $ESUDO $controlfolder/harbourmaster --quiet --no-check runtime_check "${weston_runtime}.squashfs"
    fi
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${weston_dir}"
    fi
    $ESUDO mount "$controlfolder/libs/${weston_runtime}.squashfs" "${weston_dir}"

    # Mount Godot runtime
    godot_dir=/tmp/godot
    $ESUDO mkdir -p "${godot_dir}"
    if [ ! -f "$controlfolder/libs/${godot_runtime}.squashfs" ]; then
      if [ ! -f "$controlfolder/harbourmaster" ]; then
        pm_message "This port requires the latest PortMaster to run, please go to https://portmaster.games/ for more info."
        sleep 5
        exit 1
      fi
      $ESUDO $controlfolder/harbourmaster --quiet --no-check runtime_check "${godot_runtime}.squashfs"
    fi
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${godot_dir}"
    fi
    $ESUDO mount "$controlfolder/libs/${godot_runtime}.squashfs" "${godot_dir}"


    cd $GAMEDIR
    $GPTOKEYB "$godot_executable" -c "$GAMEDIR/$gptk_filename" &

    # Start Westonpack and Godot
    # Put CRUSTY_SHOW_CURSOR=1 after "env" if you need a mouse cursor
    $ESUDO env $weston_dir/westonwrap.sh headless noop kiosk crusty_x11egl \
    XDG_DATA_HOME=$CONFDIR $godot_dir/$godot_executable \
    --resolution ${DISPLAY_WIDTH}x${DISPLAY_HEIGHT} -f \
    --rendering-driver opengl3_es --audio-driver ALSA --main-pack $GAMEDIR/$pck_filename

    #Clean up after ourselves
    $ESUDO $weston_dir/westonwrap.sh cleanup
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${weston_dir}"
        $ESUDO umount "${godot_dir}"
    fi
    pm_finish
    ```

=== "Java"
    **No GL, pure Xlib:**
    ``` bash 
    #!/bin/bash

    # PortMaster preamble
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
    get_controls

    # Adjust these to your paths and desired java version
    GAMEDIR=/$directory/ports/your_port_folder
    java_runtime="zulu17.54.21-ca-jre17.0.13-linux"
    jar_filename="YourGame.jar"
    gptk_filename="YourControls.gptk"

    # Logging
    > "$GAMEDIR/log.txt" && exec > >(tee "$GAMEDIR/log.txt") 2>&1

    # Create directory for save files
    CONFDIR="$GAMEDIR/conf/"
    $ESUDO mkdir -p "${CONFDIR}"

    # Mount Weston runtime
    weston_dir=/tmp/weston
    $ESUDO mkdir -p "${weston_dir}"
    weston_runtime="weston_pkg_0.2"
    if [ ! -f "$controlfolder/libs/${weston_runtime}.squashfs" ]; then
      if [ ! -f "$controlfolder/harbourmaster" ]; then
        pm_message "This port requires the latest PortMaster to run, please go to https://portmaster.games/ for more info."
        sleep 5
        exit 1
      fi
      $ESUDO $controlfolder/harbourmaster --quiet --no-check runtime_check "${weston_runtime}.squashfs"
    fi
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${weston_dir}"
    fi
    $ESUDO mount "$controlfolder/libs/${weston_runtime}.squashfs" "${weston_dir}"

    # Mount Java runtime
    export JAVA_HOME="/tmp/javaruntime/"
    $ESUDO mkdir -p "${JAVA_HOME}"
    if [ ! -f "$controlfolder/libs/${java_runtime}.squashfs" ]; then
      if [ ! -f "$controlfolder/harbourmaster" ]; then
        pm_message "This port requires the latest PortMaster to run, please go to https://portmaster.games/ for more info."
        sleep 5
        exit 1
      fi
      $ESUDO $controlfolder/harbourmaster --quiet --no-check runtime_check "${java_runtime}.squashfs"
    fi
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${JAVA_HOME}"
    fi
    $ESUDO mount "$controlfolder/libs/${java_runtime}.squashfs" "${JAVA_HOME}"
    export PATH="$JAVA_HOME/bin:$PATH"


    cd $GAMEDIR
    $GPTOKEYB "java" -c "$GAMEDIR/$gptk_filename" &

    # Start Westonpack and Java
    $ESUDO env $weston_dir/westonwrap.sh drm gl kiosk system \
    PATH="$PATH" JAVA_HOME="$JAVA_HOME" XDG_DATA_HOME="$GAMEDIR" WAYLAND_DISPLAY= \
    java -jar $GAMEDIR/$jar_filename

    #Clean up after ourselves
    $ESUDO $weston_dir/westonwrap.sh cleanup
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${weston_dir}"
        $ESUDO umount "${JAVA_HOME}"
    fi
    pm_finish
    ```



    **OpenGL 2.1, through Mesapack/VirGL:**
    ``` bash 
    #!/bin/bash

    # PortMaster preamble
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
    get_controls

    # Adjust these to your paths and desired java version
    GAMEDIR=/$directory/ports/your_port_folder
    java_runtime="zulu17.54.21-ca-jre17.0.13-linux"
    jar_filename="YourGame.jar"
    gptk_filename="YourControls.gptk"

    # Logging
    > "$GAMEDIR/log.txt" && exec > >(tee "$GAMEDIR/log.txt") 2>&1

    # Create directory for save files
    CONFDIR="$GAMEDIR/conf/"
    $ESUDO mkdir -p "${CONFDIR}"

    # Mount Weston runtime
    weston_dir=/tmp/weston
    $ESUDO mkdir -p "${weston_dir}"
    weston_runtime="weston_pkg_0.2"
    if [ ! -f "$controlfolder/libs/${weston_runtime}.squashfs" ]; then
      if [ ! -f "$controlfolder/harbourmaster" ]; then
        pm_message "This port requires the latest PortMaster to run, please go to https://portmaster.games/ for more info."
        sleep 5
        exit 1
      fi
      $ESUDO $controlfolder/harbourmaster --quiet --no-check runtime_check "${weston_runtime}.squashfs"
    fi
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${weston_dir}"
    fi
    $ESUDO mount "$controlfolder/libs/${weston_runtime}.squashfs" "${weston_dir}"

    # Mount Mesa runtime
    mesa_dir=/tmp/mesa
    $ESUDO mkdir -p "${mesa_dir}"
    mesa_runtime="mesa_pkg_0.1"
    if [ ! -f "$controlfolder/libs/${mesa_runtime}.squashfs" ]; then
      if [ ! -f "$controlfolder/harbourmaster" ]; then
        pm_message "This port requires the latest PortMaster to run, please go to https://portmaster.games/ for more info."
        sleep 5
        exit 1
      fi
      $ESUDO $controlfolder/harbourmaster --quiet --no-check runtime_check "${mesa_runtime}.squashfs"
    fi
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${mesa_dir}"
    fi
    $ESUDO mount "$controlfolder/libs/${mesa_runtime}.squashfs" "${mesa_dir}"

    # Mount Java runtime
    export JAVA_HOME="/tmp/javaruntime/"
    $ESUDO mkdir -p "${JAVA_HOME}"
    if [ ! -f "$controlfolder/libs/${java_runtime}.squashfs" ]; then
      if [ ! -f "$controlfolder/harbourmaster" ]; then
        pm_message "This port requires the latest PortMaster to run, please go to https://portmaster.games/ for more info."
        sleep 5
        exit 1
      fi
      $ESUDO $controlfolder/harbourmaster --quiet --no-check runtime_check "${java_runtime}.squashfs"
    fi
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${JAVA_HOME}"
    fi
    $ESUDO mount "$controlfolder/libs/${java_runtime}.squashfs" "${JAVA_HOME}"
    export PATH="$JAVA_HOME/bin:$PATH"


    cd $GAMEDIR
    $GPTOKEYB "java" -c "$GAMEDIR/$gptk_filename" &

    # Start Westonpack and Java
    # Put CRUSTY_SHOW_CURSOR=1 after "env" if you need a mouse cursor
    $ESUDO env $weston_dir/westonwrap.sh drm gl kiosk virgl \
    PATH="$PATH" JAVA_HOME="$JAVA_HOME" XDG_DATA_HOME="$GAMEDIR" WAYLAND_DISPLAY= \
    java -jar $GAMEDIR/$jar_filename

    #Clean up after ourselves
    $ESUDO $weston_dir/westonwrap.sh cleanup
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${weston_dir}"
        $ESUDO umount "${mesa_dir}"
        $ESUDO umount "${JAVA_HOME}"
    fi
    pm_finish
    ```

=== "LibGDX"
    ``` bash 
    #!/bin/bash

    # PortMaster preamble
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
    get_controls

    # Adjust these to your paths and desired java version
    GAMEDIR=/$directory/ports/your_port_folder
    java_runtime="zulu17.54.21-ca-jre17.0.13-linux"
    jar_filename="YourGame.jar"
    gptk_filename="YourControls.gptk"

    # Logging
    > "$GAMEDIR/log.txt" && exec > >(tee "$GAMEDIR/log.txt") 2>&1

    # Create directory for save files
    CONFDIR="$GAMEDIR/conf/"
    $ESUDO mkdir -p "${CONFDIR}"

    # Mount Weston runtime
    weston_dir=/tmp/weston
    $ESUDO mkdir -p "${weston_dir}"
    weston_runtime="weston_pkg_0.2"
    if [ ! -f "$controlfolder/libs/${weston_runtime}.squashfs" ]; then
      if [ ! -f "$controlfolder/harbourmaster" ]; then
        pm_message "This port requires the latest PortMaster to run, please go to https://portmaster.games/ for more info."
        sleep 5
        exit 1
      fi
      $ESUDO $controlfolder/harbourmaster --quiet --no-check runtime_check "${weston_runtime}.squashfs"
    fi
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${weston_dir}"
    fi
    $ESUDO mount "$controlfolder/libs/${weston_runtime}.squashfs" "${weston_dir}"

    # Mount Java runtime
    export JAVA_HOME="/tmp/javaruntime/"
    $ESUDO mkdir -p "${JAVA_HOME}"
    if [ ! -f "$controlfolder/libs/${java_runtime}.squashfs" ]; then
      if [ ! -f "$controlfolder/harbourmaster" ]; then
        pm_message "This port requires the latest PortMaster to run, please go to https://portmaster.games/ for more info."
        sleep 5
        exit 1
      fi
      $ESUDO $controlfolder/harbourmaster --quiet --no-check runtime_check "${java_runtime}.squashfs"
    fi
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${JAVA_HOME}"
    fi
    $ESUDO mount "$controlfolder/libs/${java_runtime}.squashfs" "${JAVA_HOME}"
    export PATH="$JAVA_HOME/bin:$PATH"


    cd $GAMEDIR
    $GPTOKEYB "java" -c "$GAMEDIR/$gptk_filename" &

    # Start Westonpack and Java
    # Put CRUSTY_SHOW_CURSOR=1 after "env" if you need a mouse cursor
    $ESUDO env $weston_dir/westonwrap.sh headless noop kiosk crusty_glx_gl4es \
    PATH="$PATH" JAVA_HOME="$JAVA_HOME" XDG_DATA_HOME="$GAMEDIR" WAYLAND_DISPLAY= \
    java -jar $GAMEDIR/$jar_filename

    #Clean up after ourselves
    $ESUDO $weston_dir/westonwrap.sh cleanup
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${weston_dir}"
        $ESUDO umount "${JAVA_HOME}"
    fi
    pm_finish
    ```


=== "OpenGL 2 (GLX)"
    **GL4ES:**
    ``` bash 
    #!/bin/bash

    # PortMaster preamble
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
    get_controls

    # Adjust these to your paths
    GAMEDIR=/$directory/ports/your_port_folder
    game_executable="your_game.aarch64"
    gptk_filename="YourControls.gptk"
    game_libs=$GAMEDIR/libs.${DEVICE_ARCH}/:$LD_LIBRARY_PATH

    # Logging
    > "$GAMEDIR/log.txt" && exec > >(tee "$GAMEDIR/log.txt") 2>&1

    # Create directory for save files
    CONFDIR="$GAMEDIR/conf/"
    $ESUDO mkdir -p "${CONFDIR}"

    # Mount Weston runtime
    weston_dir=/tmp/weston
    $ESUDO mkdir -p "${weston_dir}"
    weston_runtime="weston_pkg_0.2"
    if [ ! -f "$controlfolder/libs/${weston_runtime}.squashfs" ]; then
      if [ ! -f "$controlfolder/harbourmaster" ]; then
        pm_message "This port requires the latest PortMaster to run, please go to https://portmaster.games/ for more info."
        sleep 5
        exit 1
      fi
      $ESUDO $controlfolder/harbourmaster --quiet --no-check runtime_check "${weston_runtime}.squashfs"
    fi
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${weston_dir}"
    fi
    $ESUDO mount "$controlfolder/libs/${weston_runtime}.squashfs" "${weston_dir}"

    cd $GAMEDIR
    $GPTOKEYB "$game_executable" -c "$GAMEDIR/$gptk_filename" &

    # Start Westonpack
    # Put CRUSTY_SHOW_CURSOR=1 after "env" if you need a mouse cursor
    $ESUDO env WRAPPED_LIBRARY_PATH=$game_libs \
    $weston_dir/westonwrap.sh headless noop kiosk crusty_glx_gl4es \
    XDG_DATA_HOME=$CONFDIR $GAMEDIR/$game_executable 

    #Clean up after ourselves
    $ESUDO $weston_dir/westonwrap.sh cleanup
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${weston_dir}"
    fi
    pm_finish
    ```
    
    **VirGL:**
    ```bash
    #!/bin/bash

    # PortMaster preamble
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
    get_controls

    # Adjust these to your paths
    GAMEDIR=/$directory/ports/your_port_folder
    game_executable="your_game.aarch64"
    gptk_filename="YourControls.gptk"
    game_libs=$GAMEDIR/libs.${DEVICE_ARCH}/:$LD_LIBRARY_PATH

    # Logging
    > "$GAMEDIR/log.txt" && exec > >(tee "$GAMEDIR/log.txt") 2>&1

    # Create directory for save files
    CONFDIR="$GAMEDIR/conf/"
    $ESUDO mkdir -p "${CONFDIR}"

    # Mount Weston runtime
    weston_dir=/tmp/weston
    $ESUDO mkdir -p "${weston_dir}"
    weston_runtime="weston_pkg_0.2"
    if [ ! -f "$controlfolder/libs/${weston_runtime}.squashfs" ]; then
      if [ ! -f "$controlfolder/harbourmaster" ]; then
        pm_message "This port requires the latest PortMaster to run, please go to https://portmaster.games/ for more info."
        sleep 5
        exit 1
      fi
      $ESUDO $controlfolder/harbourmaster --quiet --no-check runtime_check "${weston_runtime}.squashfs"
    fi
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${weston_dir}"
    fi
    $ESUDO mount "$controlfolder/libs/${weston_runtime}.squashfs" "${weston_dir}"

    # Mount Mesa runtime
    mesa_dir=/tmp/mesa
    mesa_runtime="mesa_pkg_0.1"
    if [ ! -f "$controlfolder/libs/${mesa_runtime}.squashfs" ]; then
        if [ ! -f "$controlfolder/harbourmaster" ]; then
            pm_message "This port requires the latest PortMaster to run, please go to https://portmaster.games/ for more info."
            sleep 5
            exit 1
        fi
        $ESUDO $controlfolder/harbourmaster --quiet --no-check runtime_check "${mesa_runtime}.squashfs"
    fi
    $ESUDO mkdir -p "${mesa_dir}"
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${mesa_dir}"
    fi
    $ESUDO mount "$controlfolder/libs/${mesa_runtime}.squashfs" "${mesa_dir}"

    cd $GAMEDIR
    $GPTOKEYB "$game_executable" -c "$GAMEDIR/$gptk_filename" &

    # Start Westonpack
    # Put CRUSTY_SHOW_CURSOR=1 after "env" if you need a mouse cursor
    $ESUDO env WRAPPED_LIBRARY_PATH=$game_libs \
    $weston_dir/westonwrap.sh drm gl kiosk virgl \
    XDG_DATA_HOME=$CONFDIR $GAMEDIR/$game_executable 

    #Clean up after ourselves
    $ESUDO $weston_dir/westonwrap.sh cleanup
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${weston_dir}"
    fi
    pm_finish
    ```
    

=== "OpenGL ES (EGL/X11))"

    ``` bash 
    #!/bin/bash

    # PortMaster preamble
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

    # Adjust these to your paths
    GAMEDIR=/$directory/ports/your_port_folder
    game_executable="your_game.aarch64"
    gptk_filename="YourControls.gptk"
    game_libs=$GAMEDIR/libs.${DEVICE_ARCH}/:$LD_LIBRARY_PATH

    # Logging
    > "$GAMEDIR/log.txt" && exec > >(tee "$GAMEDIR/log.txt") 2>&1

    # Create directory for save files
    CONFDIR="$GAMEDIR/conf/"
    $ESUDO mkdir -p "${CONFDIR}"

    # Mount Weston runtime
    weston_dir=/tmp/weston
    $ESUDO mkdir -p "${weston_dir}"
    weston_runtime="weston_pkg_0.2"
    if [ ! -f "$controlfolder/libs/${weston_runtime}.squashfs" ]; then
      if [ ! -f "$controlfolder/harbourmaster" ]; then
        pm_message "This port requires the latest PortMaster to run, please go to https://portmaster.games/ for more info."
        sleep 5
        exit 1
      fi
      $ESUDO $controlfolder/harbourmaster --quiet --no-check runtime_check "${weston_runtime}.squashfs"
    fi
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${weston_dir}"
    fi
    $ESUDO mount "$controlfolder/libs/${weston_runtime}.squashfs" "${weston_dir}"

    cd $GAMEDIR
    $GPTOKEYB "$game_executable" -c "$GAMEDIR/$gptk_filename" &

    # Start Westonpack
    # Put CRUSTY_SHOW_CURSOR=1 after "env" if you need a mouse cursor
    $ESUDO env WRAPPED_LIBRARY_PATH=$game_libs \
    $weston_dir/westonwrap.sh headless noop kiosk crusty_x11egl \
    XDG_DATA_HOME=$CONFDIR $GAMEDIR/$game_executable 

    #Clean up after ourselves
    $ESUDO $weston_dir/westonwrap.sh cleanup
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${weston_dir}"
    fi
    pm_finish
    ```


=== "SDL2"
    **OpenGL 2:**
    ``` bash 
    #!/bin/bash

    # PortMaster preamble
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

    # Adjust these to your paths
    GAMEDIR=/$directory/ports/your_port_folder
    game_executable="your_game.aarch64"
    gptk_filename="YourControls.gptk"
    game_libs=$GAMEDIR/libs.${DEVICE_ARCH}/:$LD_LIBRARY_PATH
    x11sdl_path="$GAMEDIR/x11sdllib/"
    # Logging
    > "$GAMEDIR/log.txt" && exec > >(tee "$GAMEDIR/log.txt") 2>&1

    # Create directory for save files
    CONFDIR="$GAMEDIR/conf/"
    $ESUDO mkdir -p "${CONFDIR}"

    # Mount Weston runtime
    weston_dir=/tmp/weston
    $ESUDO mkdir -p "${weston_dir}"
    weston_runtime="weston_pkg_0.2"
    if [ ! -f "$controlfolder/libs/${weston_runtime}.squashfs" ]; then
      if [ ! -f "$controlfolder/harbourmaster" ]; then
        pm_message "This port requires the latest PortMaster to run, please go to https://portmaster.games/ for more info."
        sleep 5
        exit 1
      fi
      $ESUDO $controlfolder/harbourmaster --quiet --no-check runtime_check "${weston_runtime}.squashfs"
    fi
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${weston_dir}"
    fi
    $ESUDO mount "$controlfolder/libs/${weston_runtime}.squashfs" "${weston_dir}"

    cd $GAMEDIR
    $GPTOKEYB "$game_executable" -c "$GAMEDIR/$gptk_filename" &

    # Start Westonpack
    # Put CRUSTY_SHOW_CURSOR=1 after "env" if you need a mouse cursor
    $ESUDO env WRAPPED_LIBRARY_PATH_MALI="$x11sdl_path" WRAPPED_PRELOAD_MALI="$x11sdl_path/libSDL2-2.0.so.0" \
    WRAPPED_LIBRARY_PATH=$game_libs \
    $weston_dir/westonwrap.sh headless noop kiosk crusty_glx_gl4es \
    WAYLAND_DISPLAY= XDG_DATA_HOME=$CONFDIR $GAMEDIR/$game_executable 

    #Clean up after ourselves
    $ESUDO $weston_dir/westonwrap.sh cleanup
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${weston_dir}"
    fi
    pm_finish
    ```

    **OpenGL ES:**
    ``` bash 
    #!/bin/bash

    # PortMaster preamble
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

    # Adjust these to your paths
    GAMEDIR=/$directory/ports/your_port_folder
    game_executable="your_game.aarch64"
    gptk_filename="YourControls.gptk"
    game_libs=$GAMEDIR/libs.${DEVICE_ARCH}/:$LD_LIBRARY_PATH
    x11sdl_path="$GAMEDIR/x11sdllib/"

    # Logging
    > "$GAMEDIR/log.txt" && exec > >(tee "$GAMEDIR/log.txt") 2>&1

    # Create directory for save files
    CONFDIR="$GAMEDIR/conf/"
    $ESUDO mkdir -p "${CONFDIR}"

    # Mount Weston runtime
    weston_dir=/tmp/weston
    $ESUDO mkdir -p "${weston_dir}"
    weston_runtime="weston_pkg_0.2"
    if [ ! -f "$controlfolder/libs/${weston_runtime}.squashfs" ]; then
      if [ ! -f "$controlfolder/harbourmaster" ]; then
        pm_message "This port requires the latest PortMaster to run, please go to https://portmaster.games/ for more info."
        sleep 5
        exit 1
      fi
      $ESUDO $controlfolder/harbourmaster --quiet --no-check runtime_check "${weston_runtime}.squashfs"
    fi
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${weston_dir}"
    fi
    $ESUDO mount "$controlfolder/libs/${weston_runtime}.squashfs" "${weston_dir}"

    cd $GAMEDIR
    $GPTOKEYB "$game_executable" -c "$GAMEDIR/$gptk_filename" &

    # Start Westonpack
    # Put CRUSTY_SHOW_CURSOR=1 after "env" if you need a mouse cursor
    $ESUDO env WRAPPED_LIBRARY_PATH_MALI="$x11sdl_path" WRAPPED_PRELOAD_MALI="$x11sdl_path/libSDL2-2.0.so.0" \
    SDL_VIDEO_X11_FORCE_EGL=1 WRAPPED_LIBRARY_PATH=$game_libs \
    $weston_dir/westonwrap.sh headless noop kiosk crusty_x11egl \
    WAYLAND_DISPLAY= XDG_DATA_HOME=$CONFDIR $GAMEDIR/$game_executable 

    #Clean up after ourselves
    $ESUDO $weston_dir/westonwrap.sh cleanup
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${weston_dir}"
    fi
    pm_finish
    ```

=== "SFML"
    **OpenGL 2:**
    ``` bash 
    #!/bin/bash

    # PortMaster preamble
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
    get_controls

    # Adjust these to your paths 
    GAMEDIR=/$directory/ports/your_port_folder
    game_executable="your_game.aarch64"
    gptk_filename="YourControls.gptk"
    game_libs=$GAMEDIR/libs.${DEVICE_ARCH}/:$LD_LIBRARY_PATH

    # Logging
    > "$GAMEDIR/log.txt" && exec > >(tee "$GAMEDIR/log.txt") 2>&1

    # Create directory for save files
    CONFDIR="$GAMEDIR/conf/"
    $ESUDO mkdir -p "${CONFDIR}"

    # Mount Weston runtime
    weston_dir=/tmp/weston
    $ESUDO mkdir -p "${weston_dir}"
    weston_runtime="weston_pkg_0.2"
    if [ ! -f "$controlfolder/libs/${weston_runtime}.squashfs" ]; then
      if [ ! -f "$controlfolder/harbourmaster" ]; then
        pm_message "This port requires the latest PortMaster to run, please go to https://portmaster.games/ for more info."
        sleep 5
        exit 1
      fi
      $ESUDO $controlfolder/harbourmaster --quiet --no-check runtime_check "${weston_runtime}.squashfs"
    fi
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${weston_dir}"
    fi
    $ESUDO mount "$controlfolder/libs/${weston_runtime}.squashfs" "${weston_dir}"

    cd $GAMEDIR
    $GPTOKEYB "$game_executable" -c "$GAMEDIR/$gptk_filename" &

    # Start Westonpack
    # Put CRUSTY_SHOW_CURSOR=1 after "env" if you need a mouse cursor
    $ESUDO env WRAPPED_LIBRARY_PATH=$game_libs \
    $weston_dir/westonwrap.sh headless noop kiosk crusty_glx_gl4es \
    XDG_DATA_HOME=$CONFDIR $GAMEDIR/$game_executable 

    #Clean up after ourselves
    $ESUDO $weston_dir/westonwrap.sh cleanup
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${weston_dir}"
    fi
    pm_finish
    ```

    **OpenGL ES 1.1:**
    ``` bash 
    #!/bin/bash

    # PortMaster preamble
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
    get_controls

    # Adjust these to your paths
    GAMEDIR=/$directory/ports/your_port_folder
    game_executable="your_game.aarch64"
    gptk_filename="YourControls.gptk"
    game_libs=$GAMEDIR/libs.${DEVICE_ARCH}/:$LD_LIBRARY_PATH

    # Logging
    > "$GAMEDIR/log.txt" && exec > >(tee "$GAMEDIR/log.txt") 2>&1

    # Create directory for save files
    CONFDIR="$GAMEDIR/conf/"
    $ESUDO mkdir -p "${CONFDIR}"

    # Mount Weston runtime
    weston_dir=/tmp/weston
    $ESUDO mkdir -p "${weston_dir}"
    weston_runtime="weston_pkg_0.2"
    if [ ! -f "$controlfolder/libs/${weston_runtime}.squashfs" ]; then
      if [ ! -f "$controlfolder/harbourmaster" ]; then
        pm_message "This port requires the latest PortMaster to run, please go to https://portmaster.games/ for more info."
        sleep 5
        exit 1
      fi
      $ESUDO $controlfolder/harbourmaster --quiet --no-check runtime_check "${weston_runtime}.squashfs"
    fi
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${weston_dir}"
    fi
    $ESUDO mount "$controlfolder/libs/${weston_runtime}.squashfs" "${weston_dir}"

    cd $GAMEDIR
    $GPTOKEYB "$game_executable" -c "$GAMEDIR/$gptk_filename" &

    # Start Westonpack
    # Put CRUSTY_SHOW_CURSOR=1 after "env" if you need a mouse cursor
    $ESUDO env CRUSTY_GLES=11 WRAPPED_LIBRARY_PATH=$game_libs \
    WRAPPED_LIBRARY_PATH_MALI=$weston_dir/lib_aarch64/graphics/mesa_x11_stub/ \ 
    $weston_dir/westonwrap.sh headless noop kiosk crusty_x11egl \
    XDG_DATA_HOME=$CONFDIR $GAMEDIR/$game_executable 

    #Clean up after ourselves
    $ESUDO $weston_dir/westonwrap.sh cleanup
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${weston_dir}"
    fi
    pm_finish
    ```

    **OpenGL ES 3.1:**
    ``` bash 
    #!/bin/bash

    # PortMaster preamble
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
    get_controls

    # Adjust these to your paths
    GAMEDIR=/$directory/ports/your_port_folder
    game_executable="your_game.aarch64"
    gptk_filename="YourControls.gptk"
    game_libs=$GAMEDIR/libs.${DEVICE_ARCH}/:$LD_LIBRARY_PATH

    # Logging
    > "$GAMEDIR/log.txt" && exec > >(tee "$GAMEDIR/log.txt") 2>&1

    # Create directory for save files
    CONFDIR="$GAMEDIR/conf/"
    $ESUDO mkdir -p "${CONFDIR}"

    # Mount Weston runtime
    weston_dir=/tmp/weston
    $ESUDO mkdir -p "${weston_dir}"
    weston_runtime="weston_pkg_0.2"
    if [ ! -f "$controlfolder/libs/${weston_runtime}.squashfs" ]; then
      if [ ! -f "$controlfolder/harbourmaster" ]; then
        pm_message "This port requires the latest PortMaster to run, please go to https://portmaster.games/ for more info."
        sleep 5
        exit 1
      fi
      $ESUDO $controlfolder/harbourmaster --quiet --no-check runtime_check "${weston_runtime}.squashfs"
    fi
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${weston_dir}"
    fi
    $ESUDO mount "$controlfolder/libs/${weston_runtime}.squashfs" "${weston_dir}"

    cd $GAMEDIR
    $GPTOKEYB "$game_executable" -c "$GAMEDIR/$gptk_filename" &

    # Start Westonpack
    # Put CRUSTY_SHOW_CURSOR=1 after "env" if you need a mouse cursor
    $ESUDO env CRUSTY_GLES=31 WRAPPED_LIBRARY_PATH=$game_libs \
    $weston_dir/westonwrap.sh headless noop kiosk crusty_x11egl \
    XDG_DATA_HOME=$CONFDIR $GAMEDIR/$game_executable 

    #Clean up after ourselves
    $ESUDO $weston_dir/westonwrap.sh cleanup
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${weston_dir}"
    fi
    pm_finish
    ```








=== "Xlib"
    ``` bash 
    #!/bin/bash

    # PortMaster preamble
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
    get_controls

    # Adjust these to your paths
    GAMEDIR=/$directory/ports/your_port_folder
    game_executable="your_game.aarch64"
    gptk_filename="YourControls.gptk"
    game_libs=$GAMEDIR/libs.${DEVICE_ARCH}/:$LD_LIBRARY_PATH

    # Logging
    > "$GAMEDIR/log.txt" && exec > >(tee "$GAMEDIR/log.txt") 2>&1

    # Create directory for save files
    CONFDIR="$GAMEDIR/conf/"
    $ESUDO mkdir -p "${CONFDIR}"

    # Mount Weston runtime
    weston_dir=/tmp/weston
    $ESUDO mkdir -p "${weston_dir}"
    weston_runtime="weston_pkg_0.2"
    if [ ! -f "$controlfolder/libs/${weston_runtime}.squashfs" ]; then
      if [ ! -f "$controlfolder/harbourmaster" ]; then
        pm_message "This port requires the latest PortMaster to run, please go to https://portmaster.games/ for more info."
        sleep 5
        exit 1
      fi
      $ESUDO $controlfolder/harbourmaster --quiet --no-check runtime_check "${weston_runtime}.squashfs"
    fi
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${weston_dir}"
    fi
    $ESUDO mount "$controlfolder/libs/${weston_runtime}.squashfs" "${weston_dir}"

    cd $GAMEDIR
    $GPTOKEYB "$game_executable" -c "$GAMEDIR/$gptk_filename" &

    # Start Westonpack
    # Put CRUSTY_SHOW_CURSOR=1 after "env" if you need a mouse cursor
    $ESUDO env WRAPPED_LIBRARY_PATH=$game_libs \
    $weston_dir/westonwrap.sh drm gl kiosk system \
    XDG_DATA_HOME=$CONFDIR $GAMEDIR/$game_executable 

    #Clean up after ourselves
    $ESUDO $weston_dir/westonwrap.sh cleanup
    if [[ "$PM_CAN_MOUNT" != "N" ]]; then
        $ESUDO umount "${weston_dir}"
    fi
    pm_finish
    ```


