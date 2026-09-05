{% set porter_count = porters | length %}
{% set total_downloads = port_stats.get('total_downloads', 0) %}
# Community

PortMaster is entirely community-run. Nobody is paid for this. Every port in the
library exists because someone decided a game should run on a handheld and then
did the work to make it happen.

That work adds up to **{{ total_port_count }} ports** from
**{{ porter_count }} porters**, downloaded
**{{ "{:,}".format(total_downloads) }} times**.

---

## Thank you

To everyone who has written a port, fixed one that broke, tested on hardware
nobody else owned, answered the same question for the hundredth time on Discord,
translated the interface, made a theme, or filed a good bug report: thank you.
PortMaster is the sum of that effort.

[:material-account-group: Meet the porters](../porters.md){ .md-button .md-button--primary }

---

## Get involved

You don't need to be a programmer to help.

**Help other players.** Most support happens on Discord, and answering the
easy questions frees up the people who can answer the hard ones.

[:fontawesome-brands-discord: Join Discord](https://discord.gg/eqjK6yNQS4){ .md-button }

**Make a port.** The porting guides cover what's possible, how to build it and
how to package it.

[:material-gamepad-variant: Start porting](../contribute/index.md){ .md-button }

**Support the project.** Donations go to infrastructure and hardware for
testing, not to individuals.

[:material-hand-heart: Open Collective](https://opencollective.com/portmaster){ .md-button }

---

## Keep up

New ports land constantly, and the news section covers releases, milestones and
the occasional deep dive into how a difficult port got working.

[:material-newspaper: Read the news](../news/index.md){ .md-button }
