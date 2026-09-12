# Engine / Framework Documentation Request

Use this template when documenting an engine or framework for PortMaster. Short,
technical answers are better than polished guesses. Include commands, file
names, links, and test results whenever possible. Write `unknown` when something
still needs verification.

The answers can be sent back as-is. They will be edited into a reader-friendly
guide after technical details have been checked.

## 1. Basic information

- Engine or framework name:
- Website:
- Source code:
- License:
- What kind of games does it run?
- Is it an engine, a framework, a runtime, or a compatibility layer?
- Which PortMaster ports already use it?

Give a short explanation of why it is or is not suitable for PortMaster. Is the
game data reusable, or must the game be rebuilt? Are native plugins required?

## 2. How does a game run?

Describe the path from the PortMaster launch script to the game:

- What executable, runtime, loader, or compatibility layer runs it?
- Is the component included in the port or downloaded as a shared runtime?
- What exact runtime name and version should new ports use?
- Which architectures are supported: `aarch64`, `armhf`, or both?
- Does it need Weston, X11, GL4ES, VirGL, software rendering, or another
  display layer?
- Does it need special audio, controller, or environment settings?
- What command actually starts the game?

Paste a small, tested launch fragment here. Do not paste the generic PortMaster
preamble unless it contains an engine-specific change.

```bash
[tested launch command or engine-specific script fragment]
```

List the meaning of any important variables or commands:

| Item | Purpose |
|---|---|
| `[runtime or variable]` | [what it provides] |
| `[runtime or variable]` | [what it provides] |

## 3. Compatibility

Which versions of the engine or framework work? Which versions do not work?
Include export targets, graphics APIs, architecture, RAM, and other limits.

| Game or engine version | PortMaster runtime or method | Architecture | Result | Notes |
|---|---|---|---|---|
| `[version]` | `[runtime]` | `[arch]` | [works / partial / fails] | [details] |

What commonly blocks a port?

- `[blocker]`: [explanation and possible workaround]
- `[blocker]`: [explanation and possible workaround]

## 4. How do you identify a game?

Explain how a porter can confirm the engine and version before starting work.

- Files or directories to look for:
- Executable or archive to inspect:
- Tool or command to use:
- Where the engine version is shown:
- How to identify the export target or architecture:

```bash
[useful inspection command, if applicable]
```

## 5. What does the port contain?

Show the smallest known working port layout. Use a real port if possible.

```
[Port Name].sh
[portname]/
├── [game data or executable]
├── [runtime files, if bundled]
├── [configuration or save directory]
├── [input mapping, if needed]
└── licenses/
    └── [license files]
```

Explain anything that is not obvious:

- `[path]`: [purpose]
- `[path]`: [purpose]
- `[path]`: [purpose]

## 6. What needs changing?

List fixes that are needed for real games. For each one, include the problem,
the solution, when it runs, and whether it changes the user's original files.

### [Fix or patch name]

- Problem:
- Solution:
- Applied: [when packaging / first launch / every launch]
- Affects the user's original files: [yes / no]
- Limitations:

```bash
[command or short code example]
```

Repeat this section for each important fix. Include resolution, graphics,
controller, save path, audio, texture, and performance fixes where relevant.

## 7. Build, files, and licensing

- Build tools and dependencies:
- Build command or build instructions:
- Source repository or release used:
- Files the user must provide:
- Files that may be redistributed in a port:
- Files that must not be redistributed:
- Licenses needed in the port:

```bash
[tested build or packaging command]
```

## 8. Test report

Only list devices and versions that were actually tested.

| Device | Firmware | Runtime / engine version | Result | Notes |
|---|---|---|---|---|
| `[device]` | `[firmware]` | `[version]` | [works / partial / fails] | [details] |

Please check:

- [ ] Clean installation starts successfully.
- [ ] Controls work, including the exit shortcut.
- [ ] Saves and configuration go to the expected location.
- [ ] The game exits cleanly and starts again.
- [ ] First-run installation or patching reports errors clearly.
- [ ] Both architectures were tested, if both are supported.

## 9. Examples and references

List useful sources for the person writing the final guide:

- Example port: [link] - [what it demonstrates]
- Example port: [link] - [what it demonstrates]
- Runtime or loader: [link]
- Technical documentation: [link]
- Build tools: [link]
- Relevant discussion or issue: [link]

## 10. Known gaps

- What is still untested?
- Which versions or devices need more work?
- Which behavior is suspected but not confirmed?
- Who should be contacted for follow-up?
