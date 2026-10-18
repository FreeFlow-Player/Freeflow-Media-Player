# FreeFlow Media Player
[![Repo Stats](https://github-stats-extended.vercel.app)](https://github.com/FreeFlow-Player/Freeflow-Media-Player)

FreeFlow is an open-source media player, licensed under the GNU GPL v3. Our aim is to give you a player that adapts to you, rather than the other way around. From the interface to the way playback behaves, FreeFlow is built to be customised, so you can shape it around how you actually watch and listen instead of settling for someone else's defaults.

FreeFlow is free in every sense: free of charge, and free as in freedom. You can use it for anything, read and change the source code, and share your improvements with others. No ads, no tracking, no lock-in, and no locked-down features. Just a fast, cross-platform player for Windows, Linux and macOS that stays open and belongs to its community.

> **Free to use. Free to change. Free to share.**

## Features

- Plays video and audio on Windows, Linux and macOS
- Clean, lightweight interface with a click-to-seek progress bar
- Built on Qt Multimedia and FFmpeg, with wide format support
- Free of ads, tracking and telemetry
- Open source under the GNU GPL v3 or later

More are on the way. See the [roadmap](#roadmap).

## Screenshots

![FreeFlow playing a video](docs/images/screenshot-main.png)

## Usage

Open a file from the **File** menu.

| Action | Shortcut |
| --- | --- |
| Play / pause | `Space` / `P` |
| Seek back / forward | `←` / `→` |
| Fullscreen | `F11` |

## Roadmap

- [x] Video and audio playback
- [x] Seek bar
- [ ] Playlist support
- [X] Subtitle and audio track selection
- [ ] Customisable themes and shortcuts
- [ ] Packaged releases for Windows, Linux and macOS

Have an idea? Open an issue or start a discussion.

## Support and community

Found a bug or have a question? Please [open an issue](https://github.com/freeflow-player/freeflow-player/issues). When reporting a problem, include your operating system, FreeFlow version and, if relevant, the format of the file that failed to play.

## Contributing

FreeFlow is built in the open, and contributions of every size are welcome. You don't need to be an expert to help: fixing a typo, reporting a bug, suggesting a feature or improving the documentation is just as valuable as writing code. If you're not sure where to start, look for issues labelled `good first issue`, or open a discussion and say hello.

If you'd like to contribute code, fork the repository, create a branch for your change and open a pull request describing what you've done and why. Please keep changes focused, follow the existing code style (we use `ruff` for linting), and add tests where it makes sense. The player core is kept separate from the user interface, so it's worth reading `docs/architecture.md` first to see where your change belongs. Full details are in [CONTRIBUTING.md](CONTRIBUTING.md).

Because FreeFlow is licensed under the GNU GPL v3, anything you contribute will be released under the same licence, keeping the project free for everyone. Please be kind and constructive in issues and reviews; we want FreeFlow to be a welcoming place for people of all backgrounds and experience levels. Whether you're translating the interface, designing icons, testing on a platform you use daily, or tackling a tricky playback bug, thank you for helping make FreeFlow better.

## Installation

FreeFlow is available for Windows, Linux and macOS. You can download it from our website at [freeflow-player.github.io](https://freeflow-player.github.io), or directly from the [GitHub Releases page](https://github.com/freeflow-player/freeflow-player/releases). Both offer the same builds, so use whichever you prefer.

Pick the download for your system:

- **Windows:** download the `.exe` installer and run it. Windows may show a SmartScreen warning for new releases, so choose "More info" and then "Run anyway".
- **macOS:** download the `.dmg`, open it and drag FreeFlow into your Applications folder. If macOS blocks the first launch, right-click the app, choose "Open", and confirm.
- **Linux:** download the `.AppImage`, make it executable (`chmod +x FreeFlow-*.AppImage`) and run it.

Prefer to run it from source? See [Building from source](#building-from-source) below.

## Building from source

FreeFlow is written in Python and uses [PySide6](https://doc.qt.io/qtforpython-6/) (Qt) for both the interface and playback. Qt Multimedia handles decoding through its bundled FFmpeg backend, so there are no extra media libraries to install.

**Requirements**

- Python 3.10 or newer
- [Git](https://git-scm.com/)
- [uv](https://docs.astral.sh/uv/) (recommended), or `pip` with a virtual environment

**Get the code and run it**

```bash
git clone https://github.com/freeflow-player/freeflow-player.git
cd freeflow-player
uv sync
uv run freeflow
```

If you prefer plain `pip`:

```bash
git clone https://github.com/freeflow-player/freeflow-player.git
cd freeflow-player
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e .
freeflow
```

You can also start it with `python -m freeflow`.

**Development**

```bash
uv sync --all-extras     # installs test and lint tools
uv run pytest            # run the tests
uv run ruff check .      # lint
```

See [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

**Troubleshooting**

- **Linux:** Qt needs a few system libraries for its window and audio support. If the app fails to start with a message about the `xcb` platform plugin, install `libxcb-cursor0` (Debian/Ubuntu) or your distribution's equivalent.
- **No sound or video for a particular file:** run `FFMPEG_LOG=1`-style debugging only if you know the codec; otherwise open an issue and include the file's format.



## Licence

FreeFlow is free software, released under the [GNU General Public License v3.0 or later](LICENSE). You're free to use it for any purpose, study and modify the source code, and share both the original and your modified versions, provided they're distributed under the same licence. See the [LICENSE](LICENSE) file for the full text.

Each source file carries an SPDX identifier (`GPL-3.0-or-later`), and the licences of third-party components are listed in [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md).

## Acknowledgements

FreeFlow wouldn't exist without the work of other open-source projects. Playback is powered by [FFMpeg](https://ffmpeg.org/), and the interface is built with [Qt](https://www.qt.io/) via [PySide6](https://doc.qt.io/qtforpython-6/). Thank you to the developers and maintainers of these projects, and to everyone who contributes to FreeFlow.