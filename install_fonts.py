#!/usr/bin/env python3
"""Cross-platform font installer for the Fonts collection.

Detects the operating system and installs all .ttf/.otf fonts found
recursively in this script's directory into the correct per-user or
system-wide font directory:

  OS        User font dir                 System font dir
  --------  ----------------------------  ---------------------------
  Windows   %LOCALAPPDATA%\\...\\Fonts       C:\\Windows\\Fonts
  macOS     ~/Library/Fonts               /Library/Fonts
  Linux     ~/.local/share/fonts          /usr/share/fonts/<name>
  BSD       ~/.local/share/fonts          /usr/local/share/fonts

Usage:
  python3 install_fonts.py               # interactive install (user scope)
  python3 install_fonts.py --system      # system-wide install (needs sudo/admin)
  python3 install_fonts.py --list        # list fonts found, install nothing
  python3 install_fonts.py --dry-run     # show what would be copied, where
  python3 install_fonts.py --scope user  # force user scope
  python3 install_fonts.py --scope system
"""

from __future__ import annotations

import argparse
import ctypes
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

FONT_EXTENSIONS = {".ttf", ".otf"}

SCRIPT_DIR = Path(__file__).resolve().parent


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

def find_fonts() -> list[Path]:
    """Return all installable font files (recursive, case-insensitive)."""
    fonts = [
        p
        for p in SCRIPT_DIR.rglob("*")
        if p.is_file() and p.suffix.lower() in FONT_EXTENSIONS
    ]
    return sorted(fonts, key=lambda p: str(p).lower())


def is_admin() -> bool:
    """True when running with elevated privileges (root/administrator)."""
    if os.name == "posix":
        return os.geteuid() == 0
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except AttributeError:
        return False


def rel_to_repo(path: Path) -> str:
    """Font path relative to the repo, for readable output."""
    try:
        return str(path.relative_to(SCRIPT_DIR))
    except ValueError:
        return str(path)


# --------------------------------------------------------------------------
# OS detection and target directories
# --------------------------------------------------------------------------

def user_font_dir() -> Path:
    system = platform.system()
    home = Path.home()

    if system == "Windows":
        base = os.environ.get("LOCALAPPDATA")
        if base:
            return Path(base) / "Microsoft" / "Windows" / "Fonts"
        return home / "AppData" / "Local" / "Microsoft" / "Windows" / "Fonts"

    if system == "Darwin":
        return home / "Library" / "Fonts"

    # Linux / BSD: follow the XDG specification
    xdg_data = os.environ.get("XDG_DATA_HOME")
    if xdg_data:
        return Path(xdg_data) / "fonts"
    return home / ".local" / "share" / "fonts"


def system_font_dir() -> Path:
    system = platform.system()

    if system == "Windows":
        return Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts"

    if system == "Darwin":
        return Path("/Library/Fonts")

    if system in ("Linux",) or "BSD" in system:
        return Path("/usr/share/fonts") if system == "Linux" else Path("/usr/local/share/fonts")

    raise RuntimeError(f"Unsupported operating system: {system!r}")


# --------------------------------------------------------------------------
# Per-OS install logic
# --------------------------------------------------------------------------

def install_font_windows(font: Path, target_dir: Path, dry_run: bool) -> bool:
    """Copy a font and register it. User fonts go to HKCU, system to HKLM."""
    dest = target_dir / font.name

    if dry_run:
        print(f"  [dry-run] would install {rel_to_repo(font)} -> {dest}")
        return True

    copied = False
    if not dest.exists():
        shutil.copy2(font, dest)
        copied = True

    # Register in the registry so Windows recognises the font
    hive = "HKCU" if target_dir == user_font_dir() else "HKLM"
    value_name = f"{font.stem} ({'OpenType' if font.suffix.lower() == '.otf' else 'TrueType'})"
    value_data = str(dest)
    key = (
        rf"{hive}\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts"
    )
    subprocess.run(
        ["reg", "add", key, "/v", value_name, "/t", "REG_SZ", "/d", value_data, "/f"],
        check=True,
        capture_output=True,
    )

    # Broadcast the font-added event so apps pick it up without a reboot
    HWND_BROADCAST = 0xFFFF
    WM_FONTCHANGE = 0x001D
    SMTO_ABORTIFHUNG = 0x0002
    try:
        ctypes.windll.user32.SendMessageTimeoutW(
            HWND_BROADCAST, WM_FONTCHANGE, 0, 0, SMTO_ABORTIFHUNG, 1000, None
        )
    except Exception:
        pass  # cosmetic only; registration is what matters

    status = "installed" if copied else "already present"
    print(f"  {status}: {rel_to_repo(font)}")
    return True


def install_font_posix(font: Path, target_dir: Path, dry_run: bool) -> bool:
    """Copy the font into the target directory and refresh the font cache."""
    dest = target_dir / font.name

    if dry_run:
        print(f"  [dry-run] would install {rel_to_repo(font)} -> {dest}")
        return True

    if dest.exists():
        print(f"  already present: {rel_to_repo(font)}")
        return True

    shutil.copy2(font, dest)
    print(f"  installed: {rel_to_repo(font)}")
    return True


def refresh_cache_linux(target_dir: Path, dry_run: bool) -> None:
    if dry_run:
        print("  [dry-run] would run: fc-cache -f")
        return
    if shutil.which("fc-cache"):
        subprocess.run(["fc-cache", "-f", str(target_dir)], check=False)
    else:
        print("  note: fc-cache not found; new fonts may need a re-login.")


def install_font_macos(font: Path, target_dir: Path, dry_run: bool) -> bool:
    return install_font_posix(font, target_dir, dry_run)


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Install all fonts in this repository for the current OS."
    )
    scope_group = parser.add_mutually_exclusive_group()
    scope_group.add_argument(
        "--system",
        action="store_true",
        help="install system-wide (requires admin/root)",
    )
    scope_group.add_argument(
        "--scope",
        choices=["user", "system"],
        help="installation scope (user is the default)",
    )
    parser.add_argument("--list", action="store_true", help="list fonts and exit")
    parser.add_argument("--dry-run", action="store_true", help="show actions only")
    parser.add_argument("--yes", "-y", action="store_true", help="skip confirmation prompt")
    args = parser.parse_args()

    fonts = find_fonts()
    if not fonts:
        print("No font files (.ttf/.otf) found.")
        return 1

    if args.list:
        print(f"{len(fonts)} fonts found:")
        for font in fonts:
            print(f"  {rel_to_repo(font)}")
        return 0

    scope = "system" if (args.system or args.scope == "system") else "user"

    if scope == "system" and not is_admin():
        print(
            "System-wide installation requires elevated privileges.\n"
            "  - Windows: re-run from an Administrator prompt\n"
            "  - macOS/Linux: re-run with sudo, or use the default user scope."
        )
        return 2

    if scope == "user":
        target_dir = user_font_dir()
    else:
        target_dir = system_font_dir()

    print(f"Detected OS:     {platform.system()}")
    print(f"Install scope:   {scope}")
    print(f"Target dir:      {target_dir}")
    print(f"Fonts to install: {len(fonts)}")
    print()

    if not args.dry_run and not args.yes:
        reply = input("Proceed? [Y/n] ").strip().lower()
        if reply not in ("", "y", "yes"):
            print("Aborted.")
            return 0

    target_dir.mkdir(parents=True, exist_ok=True)

    system = platform.system()
    installed, failed = 0, 0
    try:
        for font in fonts:
            if system == "Windows":
                ok = install_font_windows(font, target_dir, args.dry_run)
            elif system == "Darwin":
                ok = install_font_macos(font, target_dir, args.dry_run)
            else:
                ok = install_font_posix(font, target_dir, args.dry_run)
            if ok:
                installed += 1
            else:
                failed += 1
    except Exception as exc:  # noqa: BLE001 - report and exit cleanly
        print(f"ERROR while installing fonts: {exc}", file=sys.stderr)
        return 1

    if system == "Linux" or "BSD" in system:
        refresh_cache_linux(target_dir, args.dry_run)

    if failed:
        print(f"\nDone: {installed} installed, {failed} failed.")
        return 1
    print(f"\nDone: {installed} font(s) processed successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
