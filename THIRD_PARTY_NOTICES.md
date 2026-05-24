# Third-Party Notices

This document lists third-party software and documentation references used by or distributed with this project.

> ⚠️ Release checklist: If you bundle binaries in `resources/tools/`, verify versions and licenses below before publishing.

## Bundled/Referenced Software

### 1) flashrom

- Project: [flashrom/flashrom](https://github.com/flashrom/flashrom)
- Website: [flashrom.org](https://www.flashrom.org/)
- Typical license: GPL-2.0 (see upstream license files for exact terms)
- How used here: external firmware flashing tool (invoked by GUI)
- Bundled path (if included): `resources/tools/<platform>/flashrom[.exe]`

Include in release package:

- Upstream license text(s)
- Source/offer information as required by the applicable license and your distribution method

### 2) flashprog

- Project: [SourceArcade/flashprog](https://github.com/SourceArcade/flashprog)
- Website: [flashprog.org](https://flashprog.org/)
- Typical license: GPL-2.0 (see upstream license files for exact terms)
- How used here: external firmware flashing tool (invoked by GUI)
- Bundled path (if included): `resources/tools/<platform>/flashprog[.exe]`

Include in release package:

- Upstream license text(s)
- Source/offer information as required by the applicable license and your distribution method

## Python Dependencies

Python package dependencies are defined in:

- `requirements.txt`
- `requirements-build.txt`

For release builds, generate a dependency license report and include it in artifacts when required by your distribution policy.

## Fonts (Downloadable / Embedded)

- This project supports downloadable fonts from upstream sources at runtime.
- Embedded-font redistribution must be treated as a release-time compliance decision.
- In `flashgui.py`, embedded font loading is intentionally disabled by default unless explicitly enabled for a licensed font payload.

If you plan to distribute an embedded font payload, include in release artifacts:

- Exact font family name and upstream source URL
- Exact license text (e.g., OFL/MIT/etc. as applicable)
- Required attribution/notice statements
- Any reserved-name or modification conditions required by the license

## Documentation and Community References (Acknowledgements)

- [flashrom classic CLI manpage](https://www.flashrom.org/classic_cli_manpage.html)
- [flashrom FT2232 SPI notes](https://www.flashrom.org/supported_hw/supported_prog/ft2232_spi.html)
- [flashrom in-system programming guide](https://www.flashrom.org/user_docs/in_system.html)
- [iFR project](https://github.com/Jazzzny/iFR)
- [FlashromGUI project](https://github.com/KantBStoppd/FlashromGUI)

These references are acknowledged for educational/interoperability context and are not redistributed as part of this repository unless explicitly stated.

## Maintainer Notes

Before publishing a release, confirm:

1. Which third-party binaries are actually shipped.
2. Their exact versions/commit hashes.
3. Their exact license files included in the release bundle.
4. Any additional notice requirements from your platform/distribution channel.

---

This project is independent and is not affiliated with or endorsed by the `flashrom` or `flashprog` maintainers.
