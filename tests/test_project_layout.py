from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_required_files_exist() -> None:
    required = [
        "flashgui.py",
        "flashgui_legacy.py",
        "requirements.txt",
        "requirements-build.txt",
        "README.md",
        "THIRD_PARTY_NOTICES.md",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), f"Missing expected file: {rel}"


def test_required_resource_directories_exist() -> None:
    required_dirs = [
        "resources",
        "resources/chips",
        "resources/datasheets",
        "resources/icons",
        "resources/tools",
    ]
    for rel in required_dirs:
        p = ROOT / rel
        assert p.exists() and p.is_dir(), f"Missing expected directory: {rel}"


def test_no_shell_or_batch_scripts_present() -> None:
    assert not any(ROOT.glob("*.bat"))
    assert not any(ROOT.glob("*.sh"))


def test_readme_mentions_python3_workflow() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "python3 -m venv .venv" in readme
    assert "python3 -m pip install -r requirements.txt" in readme
    assert "python3 flashgui.py" in readme
