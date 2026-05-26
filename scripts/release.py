from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


def _run(cmd: list[str], *, cwd: Path) -> None:
    print("[release]", " ".join(cmd))
    subprocess.run(cmd, cwd=cwd, check=True)


def _read_version(root: Path) -> str:
    source = (root / "flashgui.py").read_text(encoding="utf-8", errors="replace")
    match = re.search(r'^VERSION\s*=\s*"([^"]+)"', source, flags=re.MULTILINE)
    if not match:
        raise RuntimeError("Could not parse VERSION from flashgui.py")
    return match.group(1).strip()


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _git_status_clean(root: Path) -> bool:
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=root,
        capture_output=True,
        text=True,
        check=True,
    )
    return not result.stdout.strip()


def _current_branch(root: Path) -> str:
    result = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=root,
        capture_output=True,
        text=True,
        check=True,
    )
    branch = result.stdout.strip()
    if not branch:
        raise RuntimeError("Could not determine the current git branch")
    return branch


def _origin_repo(root: Path) -> str:
    result = subprocess.run(
        ["git", "remote", "get-url", "origin"],
        cwd=root,
        capture_output=True,
        text=True,
        check=True,
    )
    url = result.stdout.strip()
    match = re.search(r"github\.com[:/](.+?)(?:\.git)?$", url)
    if not match:
        raise RuntimeError(f"Could not infer GitHub repo from origin URL: {url}")
    return match.group(1)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Create a GitHub release for FlashGUI and trigger the existing Windows/Linux/macOS build matrix."
        ),
    )
    parser.add_argument(
        "--version",
        help="Override the version read from flashgui.py (example: 1.1.4)",
    )
    parser.add_argument(
        "--tag-prefix",
        default="v",
        help="Git tag prefix to use before the version number (default: v)",
    )
    parser.add_argument(
        "--notes-file",
        help="Path to the release notes markdown file (defaults to release/github-release-v<version>.md)",
    )
    parser.add_argument(
        "--repo",
        help="GitHub repository in OWNER/REPO form. Defaults to the origin remote.",
    )
    parser.add_argument(
        "--allow-dirty",
        action="store_true",
        help="Allow publishing with uncommitted changes present in the working tree.",
    )
    parser.add_argument(
        "--skip-local-build",
        action="store_true",
        help="Skip the local build/packaging validation step before publishing.",
    )
    parser.add_argument(
        "--no-push",
        action="store_true",
        help="Do not push the branch and release tag to origin before creating the GitHub release.",
    )
    args = parser.parse_args()

    root = _repo_root()
    version = (args.version or _read_version(root)).strip()
    tag = f"{args.tag_prefix}{version}"
    notes_file = Path(args.notes_file) if args.notes_file else root / "release" / f"github-release-v{version}.md"
    if not notes_file.is_absolute():
        notes_file = root / notes_file

    if not notes_file.is_file():
        raise FileNotFoundError(f"Release notes not found: {notes_file}")

    if not args.allow_dirty and not _git_status_clean(root):
        raise RuntimeError("Working tree is dirty. Commit or stash changes first, or pass --allow-dirty.")

    if not args.skip_local_build:
        _run([sys.executable, "scripts/build_binaries.py"], cwd=root)

    branch = _current_branch(root)
    repo = args.repo or _origin_repo(root)

    if not args.no_push:
        _run(["git", "push", "origin", branch], cwd=root)
        _run(["git", "push", "origin", tag], cwd=root)

    release_title = f"FlashGUI {tag}"
    _run(
        [
            "gh",
            "release",
            "create",
            tag,
            "--repo",
            repo,
            "--title",
            release_title,
            "--notes-file",
            str(notes_file),
        ],
        cwd=root,
    )

    print(
        "[release] GitHub Actions should now build and attach the Windows/Linux/macOS portable artifacts for",
        tag,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())