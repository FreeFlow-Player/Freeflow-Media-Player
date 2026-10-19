# Security Policy

## Supported versions

FreeFlow is in early development. Security fixes are provided for the latest release only, so please update to the newest version before reporting an issue.

| Version        | Supported |
| -------------- | ----------|
| Latest release | ✓         |
| Older releases | ✕         |

## Reporting a vulnerability

**Please do not report security vulnerabilities through public GitHub issues, discussions or pull requests.**

Instead, use GitHub's private reporting feature:

1. Go to the [Security tab](https://github.com/freeflow-player/freeflow-player/security) of this repository.
2. Click **Report a vulnerability**.
3. Describe the issue and submit the report.

Please include as much of the following as you can:

- A description of the vulnerability and its potential impact
- Steps to reproduce it, including a sample media file if relevant
- Your operating system and FreeFlow version
- Any suggested fix, if you have one

## What to expect

FreeFlow is maintained by volunteers, so these are goals rather than guarantees:

- We aim to acknowledge your report within **7 days**.
- We'll keep you updated as we investigate, and let you know whether we consider it a vulnerability.
- Once a fix is ready, we'll release it and credit you in the release notes, unless you'd prefer to stay anonymous.

We ask that you give us reasonable time to fix the issue before disclosing it publicly.

## Scope

Examples of issues we'd like to hear about:

- Crashes or memory corruption triggered by a crafted media file
- Unsafe handling of file paths, URLs or playlists
- Problems with how FreeFlow stores or loads settings
- Flaws in our release or build process

Vulnerabilities in third-party components, such as Qt or FFmpeg, should be reported to those projects directly. If FreeFlow ships a vulnerable version of one of them, though, please let us know so we can update it.

Thank you for helping keep FreeFlow and its users safe.
