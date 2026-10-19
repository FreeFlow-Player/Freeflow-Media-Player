# Contributing to FreeFlow

Thanks for your interest in FreeFlow! Contributions of every size are welcome, from fixing a typo to adding a feature. This guide explains how to get set up and how to get your changes merged.

By taking part, you agree to follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## Ways to contribute

- **Report bugs:** open an issue with clear steps to reproduce
- **Suggest features:** open an issue or discussion explaining the problem you want solved
- **Improve the docs:** README fixes, clearer instructions and new guides all help
- **Write code:** fix bugs, add features or improve performance
- **Test:** try FreeFlow on your platform and report what you find, especially on macOS and Linux
- **Translate and design:** translations, icons and UI ideas are very welcome

New to the project? Look for issues labelled `good first issue`.

## Reporting bugs

Before opening an issue, search the existing ones to avoid duplicates. A good bug report includes:

- Your operating system and version
- Your FreeFlow version
- What you expected to happen, and what actually happened
- Steps to reproduce the problem
- The format and codec of the media file, if relevant (a small sample file is even better)
- Any error messages or log output

**Security issues** should not be reported publicly. See [SECURITY.md](SECURITY.md).

## Setting up your development environment

You'll need Python 3.10 or newer, Git and [uv](https://docs.astral.sh/uv/).

```bash
# Fork the repo on GitHub, then:
git clone https://github.com/freeflow-player/freeflow-player.git
cd freeflow-player
uv sync --all-extras
uv run freeflow
```

Useful commands:

```bash
uv run pytest               # run the tests
uv run ruff check .         # lint
uv run ruff format .        # format
```

## Making a change

1. **Discuss big changes first.** For anything large, open an issue before you start, so we can agree on the approach and you don't spend time on something we can't merge.
2. **Create a branch** from `main`, with a short descriptive name, such as `fix-seek-jump` or `add-playlist`.
3. **Keep the change focused.** One fix or feature per pull request is much easier to review.
4. **Add or update tests** where it makes sense.
5. **Run the checks** (`pytest`, `ruff check`, `ruff format`) before pushing.
6. **Open a pull request** against `main` and describe what changed and why. Link the issue it addresses, and include screenshots for visual changes.

Reviews can take a little while, as FreeFlow is maintained by volunteers. Feedback is meant to improve the change, so please don't take it personally.

## Code style

- Follow [PEP 8](https://peps.python.org/pep-0008/), enforced by `ruff`
- Use type hints on public functions and methods
- Write clear names and short functions, and add a comment where the reason for something isn't obvious
- Add this header to every new source file:

```python
  # SPDX-License-Identifier: GPL-3.0-or-later
```

## Commit messages

Write commit messages in the imperative mood, with a short summary line of about 50 characters, followed by a blank line and more detail if needed:

```Git Commit
Fix seek bar jumping back while dragging

The slider was updated by playback position events during a drag.
Ignore position updates while the slider is pressed.
```

## Licensing of contributions

FreeFlow is licensed under the [GNU GPL v3 or later](LICENSE). By submitting a contribution, you confirm that you have the right to submit it, and you agree that it will be released under the same licence.

Only add third-party code or assets if their licence is compatible with the GPL, and mention them in [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md).

## Platform testing

FreeFlow targets Windows, Linux and macOS. If your change touches playback, window handling, fullscreen or file paths, please say which platforms you tested on in your pull request. If you could only test on one, say so, and a maintainer or another contributor can check the rest.

## Questions

Not sure where to start, or unsure whether an idea fits? Open a discussion/issue or [join our discord server](https://discord.gg/amWCH8Gyqt). No question is too small.

Thank you for helping make FreeFlow better!
