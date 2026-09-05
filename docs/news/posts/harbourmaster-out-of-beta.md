---
date: 2023-07-22
authors:
  - cebion
readtime: 3
description: >
  The HarbourMaster backend leaves public beta, bringing filtering, port
  uninstallation, custom repositories and a runtime downloader.
---

# HarbourMaster leaves beta

We have been sailing the seas hard and can now take the new HarbourMaster
backend out of public beta. On your next PortMaster update you will get some
more functionality.

<!-- more -->

## Features of the new backend

* **Ability to filter games** in PortMaster.
* **Installation and uninstallation** of ports.
* **Add your own repository** for games not on PortMaster.
* **Included runtime downloader.**

With this release we laid down the cornerstones needed for the next iteration of
the PortMaster client.

## Notes for porters

Runtimes such as Mono, FRT and Java are now hosted in our
[runtime repository](https://github.com/PortsMaster/PortMaster-Runtime).

You now need to supply a `gamename.port.json` file inside your port folder, and
specify the runtime your port needs in it.

## What else is being worked on

**Rewrite of the wiki.** A proof of concept is in full swing and taking shape.
It will be optimised for desktop and mobile, with an overview page and a detail
page for each game.

**New PortMaster GUI.** We love the current design, but as we get more and more
ports we also want a more modern approach with screenshots and theme support
that can handle more titles easily. This is under active development.

**New internal game database for porters.** A simple webpage with a database
behind it, to collect and track possible port candidates and avoid duplicating
work that has already been done.
