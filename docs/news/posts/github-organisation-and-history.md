---
date: 2024-02-03
authors:
  - cebion
readtime: 7
description: >
  PortMaster moves to its own GitHub organisation, and a look back at how it
  grew from around 40 ports to over 320.
---

# A new home on GitHub, and how we got here

Today a big milestone was reached by migrating PortMaster to our new GitHub
organisation, and we want to share it with you.

<!-- more -->

PortMaster emerged as an alternative to AnberPorts, originally created by
christianhaitian, initially designed as a straightforward tool akin to
JohnIrvine's ThemeMaster themes management utility. Sporting a text-based user
interface, PortMaster aimed to streamline the process of downloading ports for
various systems including 351Elec, ArkOS, JelOS, RetroOZ and TheRA on RK3326
based devices.

Over the course of two and a half years, PortMaster has grown from a modest
collection of around 40 ports to an extensive repository of over 320.

## Early stages

Initially PortMaster relied on a simple text file to catalog its ports, with the
repository consisting of basic zip files. As the number of ports passed 80, the
repository moved to GitHub actions for releasing updates thanks to pkegg,
enabling the inclusion of larger ports exceeding GitHub's 100MB file size limit.

As PortMaster grew, development occurred primarily on the AmberELEC server,
where enthusiasts congregated to discuss and contribute to the project.

## Growth and innovations

Around the time PortMaster reached 120 ports, it faced scalability issues,
leading to the creation of HarbourMaster. This package manager, spearheaded by
kloptops, aimed to improve port management. HarbourMaster introduced port
uninstallation, genre-based filtering and, crucially, runtime support, making it
much easier to include games developed in Godot.

The launch of HarbourMaster coincided with the establishment of a dedicated
Discord server and the start of GUI development by kloptops and tekkenfedde. A
new website, crafted by various members under the leadership of Bamboozler,
aimed to replace the previous single page wiki.

## Leap forward

Around 180 ports, PortMaster introduced its highly anticipated GUI and launched
the new website, marking a significant leap in discoverability and
accessibility. The debut of the GUI also welcomed new porters, mattyj and
tabreturn, who contributed a substantial 50 ports within weeks.

## Challenges and solutions

Despite its success, PortMaster ran into problems caused by relying on zipped
files inside a git repository. Updates were error-prone and changes within zip
files were difficult to track.

The fix was to transition the repository to unzipped ports. This improved
release cycles, notably reducing upload times and preventing repository size
inflation. A script was introduced to divide large files into manageable chunks,
so they could live inside the git repository instead of outside it.

Despite initial concerns about repository size, ongoing updates have shown the
efficiency and scalability of the new system, with minimal impact on storage.

## Thanks

Special gratitude goes to **Christian Haitian** for his invaluable
contributions and patience with the project. His meticulous attention to proper
attribution and diligent review of PRs have left a lasting impact. Although he
has taken a step back, his influence continues to guide us. We also owe him
recognition for creating the best port on PortMaster: 2048.

We also thank:

* **Cebion**, for exceptional leadership among porters, prolific submissions,
  and unwavering support through guides, FAQs and assistance.
* **JohnnyOnFlame**, for delivering top-notch ports and patching games to ensure
  compatibility with devices' limited performance.
* **romadu** and **Jetup**, for the groundwork in bringing all-time beloved
  ports to PortMaster.
* **kreal**, for being an innovator and visionary who showed us what ports could
  become.
* **kloptops**, for spearheading the HarbourMaster package manager, the new GUI
  and the revamped repository.
* **Bamboozler**, for crafting the website and for being the second-highest
  porter in PortMaster.
* **tekkenfede**, for invaluable help designing the new GUI, creating themes and
  porting numerous titles.
* **mattyj513**, for a whirlwind of submissions, delivering 34 ports in a
  remarkably short time before stepping back due to health issues.
* **tabreturn**, for porting help, relentless testing and port submissions.

We extend our gratitude to countless others who have shaped the project into
what it is today. Thank you all.
