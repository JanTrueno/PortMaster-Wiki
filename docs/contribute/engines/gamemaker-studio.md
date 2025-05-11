# GameMaker Studio


_[GameMaker Studio](https://gamemaker.io/en) is a game development engine designed to simplify the creation of 2D games. It offers a drag-and-drop interface for beginners and a custom scripting language for advanced users. Developers can create game elements through an event-driven system, making the engine accessible without requiring extensive programming knowledge._

_While GameMaker supports multiple platforms, including Windows, macOS, Linux, Android, iOS, and major consoles like Nintendo Switch, PlayStation, and Xbox, its support for ARM-based Linux systems is extremely limited. As a result, GameMaker titles are not compatible with the handheld devices supported by PortMaster using conventional methods._

## Porting Methodology


[Gmloader](https://github.com/JohnnyonFlame/droidports) and its successor, [gmloader-next](https://github.com/JohnnyonFlame/gmloader-next) are GameMaker Studio compatibility layers for ARM-based Linux systems, developed by [JohnnyOnFlame](https://github.com/JohnnyonFlame) and contributors. These projects share a history and codebase to the PS Vita parallel project, [YoYoLoader](https://github.com/Rinnegatamante/yoyoloader_vita).

Both gmloader and gmloader-next function as compatibility layers for `libyoyo.so`, the official GameMaker Studio Runner application for Android. They load the ARM executable into memory, resolve its imports with native functions, and apply necessary patches to ensure proper execution.

By simulating a minimalist Android-like environment, these tools enable the native execution of GameMaker Studio-developed games on ARM-based Linux devices.

For more details on gmloader’s origin and deeper technical functionality, refer to the [research documentation](https://github.com/JohnnyonFlame/yyg_fix/blob/master/RESEARCH.md).

#Compatibility


The theoretical compatibility across platforms is summarized in the table below:

| Platform | Bytecode Compiler | YoYo Compiler (YYC) |
|----------|-------------------|---------------------|
| Android  | Yes               | Yes                 |
| Windows  | Yes               | No                  |
| Linux    | Yes               | No                  |
| macOS    | Yes               | No                  |

*   **gmloader**: Supports GMS versions **2022.x** and earlier, compatible with **ARMv7/armhf** architectures.
*   **gmloader-next.armhf**: Supports **all GMS versions**, works with **ARMv7/armhf**.
*   **gmloader-next.aarch64**: Supports GMS version **2.2.1+**, compatible with **ARMv8/AARCH64**.

### What is YYC?

**YYC** (YoYo Compiler) is a feature in GameMaker Studio that compiles game code directly into machine code. This process leads to:

*   **Faster execution speed**.
*   **Enhanced security** due to direct compilation.
*   However, the compiled code is integrated tightly into the executable, **reducing portability** across different platforms.

### Determining GMS Version and Compiler Type

To determine whether a GameMaker game uses **YYC** or **bytecode**, follow these steps:

1.  **Install UndertaleModTool** from [here](https://github.com/UnderminersTeam/UndertaleModTool/releases).
2.  **Extract game assets** (e.g., `data.win`, `game.unx`, `game.ios`, or `game.droid`) from the APK using [7Zip](https://www.7-zip.org/download.html).
3.  **Open the extracted assets** in **UndertaleModTool**. The tool will automatically detect if the game uses **YYC** or **bytecode**.
4.  Navigate to **Data > General Info** to check the **GameMaker version**.

If the game uses **YYC**, a warning will appear in UndertaleModTool.

Steps Involved
==============

Porting a **GameMaker** game to an ARM-based Linux device using **gmloader** involves several key steps. The following guide outlines the process for porting a game.

### Step 1: Find the Target Game

The first step is to select a **GameMaker** game to port. A variety of GameMaker-developed games can be found on the following platforms:

*   [**Itch.io**: Games made with GameMaker](https://itch.io/games/made-with-gamemaker)
*   [**SteamDB**: Steam games using GameMaker Studio](https://steamdb.info/tech/Engine/GameMaker/)

Tags and filters can be used to narrow down the search. It is recommended to begin with free games, as most commercially successful portable games have already been ported.

### Step 2: Extract the Game’s Bytecode File

After selecting the game, the next step is to locate its bytecode file. GameMaker games typically store their assets in files such as **data.win**, **game.unx**, **game.ios**, or **game.droid**.

To extract and inspect these files:

1.  **Download UndertaleModTool** from [here](https://github.com/UnderminersTeam/UndertaleModTool/releases).
2.  **Extract the game files** from the APK or game folder.
3.  **Open the bytecode file** (e.g., **data.win**, **game.unx**, **game.ios**,or **game.droid**) with UndertaleModTool.

### Step 3: Check for YYC and GameMaker Version

Within **UndertaleModTool**, check if the game uses **YYC (YoYo Compiler)** or bytecode:

1.  Look for the **YYC warning**. If the game uses YYC, a warning will appear.
2.  Check the **GameMaker version** under _Data > General Info_.

**Note**: UndertaleModTool makes an educated guess regarding the version, so accuracy is not always guaranteed.

### Step 4: Select the Correct Wrapper

After confirming the GameMaker version and compiler type, the appropriate wrapper APK should be downloaded from the following repository:

*   [**GameMaker Studio Wrappers**: wrapper APKs](https://github.com/Fraxinus88/GMloader-ports/tree/main/gmloader%20wrappers%20(APK))

**Note**: It is preferable to **build a custom wrapper/APK** for final packaging. This can be done by downloading the matching version of GameMaker Studio, setting up the Android export, and exporting an open-source example. After the first launch, the assets can be removed using the following command: `zip -d portname.port 'assets/*'`. For further details on the reasoning behind this packaging, refer to the documentation below.

### Step 5: Rework the Example Package for the Game

After obtaining the correct wrapper, the example zip package must be reworked for the specific game. Depending on the version of GameMaker Studio (GMS) used, choose between the following:

*   **gmloader** (deprecated unless necessary)
*   **gmloadernext.aarch64** (recommended for GMS 2.2.1+ on ARMv8)
*   **gmloadernext.armhf** (recommended for GMS 2.2.1- on ARMv7)

It is crucial to ensure that the selected wrapper/APK includes the appropriate, matching, ARMv7 or ARMv8 Android libraries.

By following these steps, a GameMaker game can be ported to an ARM-based Linux device using **gmloader**. Some games may require additional troubleshooting or configuration to run properly on the target device.

Packaging
=========

### GMLoader Port File Structure

    - Portname.sh
    - portname/
    	- lib/
    		- armv8a 
    		- armv7a
    		- libopenal.so.1
    		- libzip.so.5
    		- libcrypto.so.1
    	- assets/
    	    - .gitkeep
    	- saves/
    		- .gitkeep
    	- gmloader.json
    	- patches/
    		- patchscript 
    	- portname.gptk
    	- portname.port
    

*   **lib folder**  
    The `lib` folder within the runtime squashfs houses Android AOSP libraries, taken from a prebuilt image provided by Google. This folder is named `lib` because these are native Android libraries, following the file path structure used in Android. The `libs.${DEVICE_ARCH}` folder contains libraries native to either `aarch64` or `armhf`. GMLoader-Next requires `libcrypto`, `libopenal`, and `libzip` at a minimum to function.
    
*   **licenses folder**  
    The `licenses` folder contains text and markdown files that outline the license agreements for each library and binary used in GMLoader.
    
*   **assets folder**  
    This folder is where the end users place their game data. Typically, users will copy everything from their Steam or GOG installation folder, or unzip an archive from [Itch.io](http://Itch.io) into this folder. Once the `patchscript` completes on the first run, this folder may be removed.
    
*   **saves folder**  
    This folder is used to store GameMaker games’ save data. While the folder can be renamed, it is typically referred to as `saves`.
    
*   **gmloader.json**  
    This JSON file contains configuration options for GMLoader-Next on a per-port basis. It is configurable and can be named `portname.json`.
    

    {
        "save_dir" : "saves",
        "apk_path" : "my_game.port",
        "show_cursor" : false,
        "disable_controller" : false,
        "force_platform" : "os_windows"
    }
    

*   **patchscript**  
    This is a bash script that runs on the first boot via the PortMaster Patcher program. The `.sh` file extension is avoided to prevent interference with PortMaster scripts. An example of the script can be found [here](https://github.com/JeodC/PortMaster-UFO50/blob/main/ufo50/tools/patchscript).
    
*   **portname.gptk**  
    If the GpToKeyB tool is used in the port, this file is likely included. Even if native gamepad controls are present, it is still advisable to include an empty `portname.gptk` file for debugging.
    

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
    

*   **portname.port**  
    This is an archive file structured like an APK file but without any Android-specific references. Upon opening, it will contain a `lib` folder with the GameMaker Studio runtime file and, if the port has been packed, an `assets` folder containing all the game data previously stored in the `portname/assets` folder.

**Note:**  
Game Maker Studio has listed two end-user license agreements on their website for their runtimes: the [free](https://gamemaker.io/en/legal/gamemaker-runtime-licence-free) agreement, and the [professional](https://gamemaker.io/en/legal/gamemaker-runtime-licence-professional) agreement. Both list the following clause:

> This licence grants you the right to distribute the runtime portion of GameMaker in executable code format only as an integrated and inseparable part of your content to third parties to whom you license such content, subject in each case to your full compliance with the GameMaker Terms and payment of all applicable fees.

In order to adhere to the EULA, we execute a good-faith practice by bundling game data with the runtime inside the `portname.port` archive.

Patching and known bugs
=======================

Sometimes ports need patches to function properly. Patches can be created with UTMT and In-house tools from Portmaster. Patches are usually deployed with an xdelta patch. When patching takes long it’s recommended to use the PortMaster patching program to show progress.

### Pack audio into wrapper:

Gmloader can have **trouble loading in the audio** when they are not packed into the wrapper/apk. The following example script will pack the OGG’s to the wrapper/apk. This can also be adapted for games that use audiogroups.

    # Check for .ogg files and move to APK
    	if [ -n "$(ls ./assets/*.ogg 2>/dev/null)" ]; then
        zip -r -0 ./portname.port./assets/
        echo "Zipped contents to ./portname.port"
    else
        echo "No .ogg files found"
    fi
    

### NewTextureRepacker (UTMT)

Script to export and repack textures developed by JohnnyOnFlame. Known to **fix crashes caused by huge texturepages** on Mali gpu’s. Can **reduce ram usage**. Known to **fix broken fonts** on Mali gpu’s.

### Bytecode up/downgraders (UTMT)

This collection of scripts can up and downgrade bytecode versions. This can **increase compatibility** for GMS1 and GMS2 games.

### GMTools (PortMaster In-house)

Not all GameMaker games are the same when it comes to audio. Developers have a variety of audio options, from streaming external audio (like Undertale), to grouping audio files into `audiogroup.dat` files, to embedding audio files into the GMS data file. When audio files aren’t streamed, they’re loaded into memory at runtime. For low-mem handhelds, this can cause problems. GMTools analyzes all audiogroups and the data file and converts any `.wav` files it finds to `.ogg`, and can also compress audio to a specified bitrate. This can significantly **reduce ram usage**. For our usecase, audio quality isn’t a big concern–the handhelds use small speakers, after all.

### Patch deployment (PortMaster tool)

If a GMS data file requires modifications, we need to then supply a method for the end-user to make use of the modifications without having to open up UTMT themselves. PortMaster strives to make ports as accessible and seamless as possible. [XDelta3](https://github.com/Moodkiller/xdelta3-gui-2.0) both creates a patch file containing the differences between our two GMS data files, and applies patch files on-device during the first-time launch process for a port. This can be done with out xdelta binary inside the PortMaster controlfolder using the following:

    # Check if "data.win" exists and its MD5 checksum matches the specified value then apply patch
    if [ -f "assets/data.win" ]; then
        checksum=$(md5sum "assets/data.win" | awk '{print $1}')
        if [ "$checksum" = "4b97bb2da8c515d787fe70aa03550ce5" ]; then
            $ESUDO $controlfolder/xdelta3 -d -s "assets/data.win" -f "./patch/patch.xdelta3" "assets/game.droid" && \
            rm "assets/data.win"
        fi
    fi
    

Tools Used
==========

PortMaster Engineers heavily rely on a few major tools that make GMS ports successful.

*   [GameMaker Studio](https://gamemaker.io/en) is the **game engine** in which these games are created. If a GMS game is open source, we can use GMS to build it ourselves and make it “Ready To Run”. Example: [Spelunky Classic HD](https://github.com/JanTrueno/SpelunkyClassicHD).
    
*   [UndertaleModTool](https://github.com/UnderminersTeam/UndertaleModTool) is a fantastic tool for both **examining GameMaker files** (`data.win`, `game.unx`, `game.ios` and `game.droid`) and **modifying them** via scripts.
    
*   [XDelta3 GUI](https://github.com/Moodkiller/xdelta3-gui-2.0) is a gui version of xdelta3 that allows **creating `.xdelta` patch files** from differences in two files, used for GameMaker game modifications. A cli variant exists in PortMaster for applying these patches to legally obtained game files.
    
*   [GMTools](https://github.com/cdeletre/gmtools), by PortMaster Crew Member Cyril aka kotzebuedog, is a python script that handles **audio analysis and compression**.
    
*   [GMLoader](https://github.com/JohnnyonFlame/droidports) and [GMLoader-Next](https://github.com/JohnnyonFlame/gmloader-next) are the **compatibility binaries** that translate android vm bytecode to linux vm. These two (used for armhf and aarch64 respectively) read an android GameMaker runner library `libyoyo.so` and translate it for linux execution.
    

Troubleshooting Performance (Case Study)
========================================

**UFO50:**

> When ram limitations are not the problem, it’s time to dive deeper to find out why the game performs subpar. GameMaker uses rooms as a space  
> to load content–and will often contain preplaced static content such  
> as tiles to avoid draw calls later. A game can have several different  
> rooms, like one for the title screen, and then another for the game  
> itself, etc. These rooms are loaded into memory wholesale, so if a  
> room has massive dimensions (think 10,000 x 20,000), it might also  
> have a massive amount of object instances. This means the entire game  
> will chug while using that room. A good example of this is UFO 50’s  
> Ninpek game. If we open UFO 50 in UndertaleModTool and load  
> `rm34_Ninpek`, we can instantly see why it’s choppy and slow on  
> small-arm handhelds: the room dimensions are 15,360 x 216. Ninpek is a  
> sidescrolling game with a constantly moving camera, so it’s natural  
> for the developer to create a room like this to hold the content and  
> flow. However, because the room contains so many instances, it slows  
> to a crawl on low-power devices. There’s not much we can do about a  
> room like this, though, at least not without heavily tampering with  
> the game–which would essentially deviate the project from a simple  
> compatibility patch and turn it into a complete mod.

**Isles of Sea and Sky:**

> Isles of Sea and Sky is another fine example of performance  
> troubleshooting. In IOSAS, entering specific areas will result in a  
> huge framerate drop–which instantly recovers as soon as the area is  
> left. This again indicates a problem with rooms. IOSAS has a specific  
> set of rooms called “god rooms” that load a specific script that has  
> to do with “god gem” special effects. This special effect in question  
> is a calculation loop for drawing lines to synchronize with gems  
> rotating around a sprite. Calculations are already cpu-intensive  
> tasks, so putting them into a loop that executes every frame is asking  
> for low performance. This particular case was resolved by modifying  
> the loop to retrieve variables from a file `pm-config.ini`, an ini  
> file specially made for the port. Inside, the user can configure two  
> variables: `Idol_SFX` and `FrameSkip`. If `Idol_SFX=1`, meaning the  
> loop is allowed to execute, then `FrameSkip=x` will dictate when the  
> loop will execute. Instead of executing every frame (`FrameSkip=0`),  
> we can modify the value so the loop only executes every 20 or 30  
> frames. This results in a change: our low framerate is now a stutter,  
> where the game “pauses” once every x frames when it performs the  
> calculation step. This means the special effect also isn’t perfectly  
> aligned–but it preserves the artistic effect somewhat while  
> compensating for low cpu power.

Compiling
=========

Gmloader-next can be cross-compiled using the following steps. This is for development and contribution only, prebuilds are available in the example packages.

    # Clone the repository and all submodules
    git clone https://github.com/JohnnyonFlame/gmloader-next --recursive  
    
    # Build the project with desired target platform options  
    make -f Makefile.gmloader ARCH=aarch64-linux-gnu  
    
    # Example: Build using Debian Bullseye for older platforms  
    make -f Makefile.gmloader \
      ARCH=aarch64-linux-gnu \
      LLVM_FILE=/usr/lib/llvm-11/lib/libclang-11.so.1 \
      LLVM_INC=/usr/aarch64-linux-gnu/include/c++/10/aarch64-linux-gnu \
      -j$(nproc)  
    
    # Generate the libc dependencies  
    python3 scripts/generate_libc.py aarch64-linux-gnu \
      --llvm-includes /usr/aarch64-linux-gnu/include/c++/10/aarch64-linux-gnu \
      --llvm-library-file "/usr/lib/llvm-11/lib/libclang-11.so.1"  
    
    # Deploy: Copy the lib redist folder to the application directory  
    cp -r lib_redist/ <application_folder>/  
    
    # For more details, check the documentation  
    xdg-open https://github.com/JohnnyonFlame/gmloader-next
    

Conclusion
==========

By leveraging the tools and knowledge outlined in this guide, PortMaster Engineers enable modern **GameMaker Studio** games to run smoothly on small ARM-based handheld devices. The primary focus is on preserving the original game’s features and feel, while optimizing it for different hardware. These optimizations help ensure that these iconic titles reach new platforms and players.

Some of the notable games ported include:

*   **Undertale**
*   **AM2R (Another Metroid 2 Remake)**
*   **Forager**
*   **UFO50**
*   **Risk of Rain**

Through these efforts, we strive to make **GameMaker Studio** games accessible to a wider audience, ensuring they remain playable on a variety of devices.
