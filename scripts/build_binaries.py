from __future__ import annotations

import argparse
import importlib.util
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


def _detect_target() -> str:
    p = sys.platform
    if p.startswith("win"):
        return "windows"
    if p.startswith("linux"):
        return "linux"
    if p == "darwin":
        return "macos"
    raise RuntimeError(f"Unsupported platform: {p}")


def _normalize_arch() -> str:
    m = platform.machine().lower()
    mapping = {
        "amd64": "x64",
        "x86_64": "x64",
        "x64": "x64",
        "arm64": "arm64",
        "aarch64": "arm64",
    }
    return mapping.get(m, re.sub(r"[^a-z0-9]+", "", m) or "unknown")


def _project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _read_version(root: Path) -> str:
    source = (root / "flashgui.py").read_text(encoding="utf-8", errors="replace")
    m = re.search(r'^VERSION\s*=\s*"([^"]+)"', source, flags=re.MULTILINE)
    if not m:
        raise RuntimeError("Could not parse VERSION from flashgui.py")
    return m.group(1).strip()


def _resolve_icon(root: Path) -> Path:
    ico = root / "resources" / "icons" / "flashgui.ico"
    if ico.is_file():
        return ico
    raise RuntimeError(f"Icon not found: {ico}")


def _ensure_pyinstaller_available() -> None:
    """Fail fast with actionable guidance when PyInstaller is not installed."""
    if importlib.util.find_spec("PyInstaller") is not None:
        return

    hints = [
        "PyInstaller is not installed for the interpreter running this script.",
        f"Current interpreter: {sys.executable}",
        "Install it in this environment (for example: pip install -r requirements-build.txt).",
    ]

    if sys.platform.startswith("win") and "msys64" in str(Path(sys.executable)).lower():
        hints.append(
            "On Windows, 'python3' may point to MSYS Python. Prefer running this script with 'python' from your project venv."
        )

    raise RuntimeError(" ".join(hints))


def _run_pyinstaller(root: Path, name: str, icon: Path) -> Path:
    _ensure_pyinstaller_available()
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--onefile",
        "--name",
        name,
        "--icon",
        str(icon),
        "flashgui.py",
    ]
    print("[build] Running:", " ".join(cmd))
    subprocess.run(cmd, cwd=root, check=True)

    ext = ".exe" if _detect_target() == "windows" else ""
    out_bin = root / "dist" / f"{name}{ext}"
    if not out_bin.is_file():
        raise RuntimeError(f"Build completed but output not found: {out_bin}")
    return out_bin


def _copy_if_exists(src: Path, dst: Path) -> None:
    if not src.exists():
        return
    if src.is_dir():
        shutil.copytree(src, dst / src.name, dirs_exist_ok=True)
    else:
        dst.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst / src.name)


def _zip_dir(src_dir: Path, zip_path: Path) -> Path:
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(zip_path, "w", compression=ZIP_DEFLATED) as zf:
        for p in sorted(src_dir.rglob("*")):
            if p.is_dir():
                continue
            zf.write(p, arcname=p.relative_to(src_dir))
    return zip_path


def _package_release_artifacts(
    root: Path,
    binary_path: Path,
    version: str,
    target: str,
    arch: str,
    *,
    include_screenshots: bool = True,
) -> Path:
    release_dir = root / "release"
    release_dir.mkdir(parents=True, exist_ok=True)

    artifact_base = f"flashgui-v{version}-{target}-{arch}"
    portable_name = f"{artifact_base}-portable"

    portable_stage = release_dir / portable_name
    app_folder_name = "flashgui"

    if portable_stage.exists():
        shutil.rmtree(portable_stage)

    portable_app = portable_stage / app_folder_name
    portable_app.mkdir(parents=True, exist_ok=True)
    shutil.copy2(binary_path, portable_app / binary_path.name)
    _copy_if_exists(root / "resources", portable_app)
    if include_screenshots:
        _copy_if_exists(root / "screenshots", portable_app)
    for rel in (
        "README.md",
        "LICENSE",
        "THIRD_PARTY_NOTICES.md",
        "RELEASE_NOTES.md",
        "MANUAL_QA_CHECKLIST.md",
        "flashgui_settings.json",
    ):
        _copy_if_exists(root / rel, portable_app)

    portable_zip = release_dir / f"{portable_name}.zip"
    _zip_dir(portable_stage, portable_zip)
    return portable_zip


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build FlashGUI portable one-file binaries on Windows/Linux/macOS using PyInstaller.",
    )
    parser.add_argument(
        "--target",
        choices=["auto", "windows", "linux", "macos"],
        default="auto",
        help="Target platform label. Use 'auto' to detect from current OS.",
    )
    parser.add_argument(
        "--no-screenshots",
        action="store_true",
        help="Exclude screenshots/ from release bundle.",
    )
    args = parser.parse_args()

    host_target = _detect_target()
    target = host_target if args.target == "auto" else args.target
    if target != host_target:
        raise RuntimeError(
            f"Requested target '{target}' does not match host OS '{host_target}'. "
            "Cross-compiling is not supported by this script."
        )

    root = _project_root()
    version = _read_version(root)
    arch = _normalize_arch()
    icon = _resolve_icon(root)

    build_name = f"flashgui-{target}-{arch}"

    dist_bin = root / "dist" / (build_name + (".exe" if target == "windows" else ""))
    if dist_bin.exists():
        dist_bin.unlink()

    build_dir = root / "build" / build_name
    if build_dir.exists():
        shutil.rmtree(build_dir)

    output = _run_pyinstaller(root, build_name, icon)
    portable_zip = _package_release_artifacts(
        root,
        output,
        version,
        target,
        arch,
        include_screenshots=not args.no_screenshots,
    )

    print(f"[build] Output binary: {output}")
    print(f"[build] Portable archive: {portable_zip}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"[build] ERROR: {exc}")
        raise SystemExit(1)
