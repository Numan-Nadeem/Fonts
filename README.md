# 🎨 My Font Collection 🎨

> A curated collection of beautiful and unique fonts for all your design needs.

This repository is a personal collection of fonts that I have gathered over time. I use them for various projects, from web design to print media. I hope you find them as useful as I do!

---

## ✒️ The Fonts

Here is a list of the font families available in this collection.

### ✨ Austral Sans
A beautiful and unique font.

### ✨ Berkeley Mono
Berkeley Mono is a modern, versatile monospace typeface specifically designed for coding and professionals, aiming for a machine-readable aesthetic where accuracy was prioritized.

### ✨ Bowlby One
A stunning and eye-catching font.

### ✨ Coolvetica
Coolvetica is a sans-serif typeface inspired by the groovy era of the 1970s. It recreates the custom display lettering style of that decade, characterized by extra-tight kerning and playful curls.

### ✨ Hand Originals
The 'Hand Originals' font is a hand-drawn typeface characterized by a playful, informal, and expressive style with thick strokes and slightly irregular characters, giving it a handcrafted feel.

### ✨ Lemonmilk
A fresh and modern font.

### ✨ MartianMono
A great font for a variety of uses.

### ✨ Mehr Nastaliq Web Regular
The Mehr Nastaliq Web Regular font is an OpenType Urdu Nastaliq font. It follows the traditional Nastaliq calligraphy, known for its elegant appearance with diagonal or oblique letterforms.

### ✨ Montserrat
Montserrat is a geometric sans-serif typeface inspired by posters, signs, and painted windows from the first half of the twentieth century, seen in the historic Montserrat neighborhood of Buenos Aires.

### ✨ San Francisco Pro
San Francisco Pro (SF Pro) is Apple's system typeface for macOS, iOS, and iPadOS, designed for optimal legibility and neutrality across display and text sizes. This collection includes the full **Text**, **Display**, and **Rounded** families in 9 weights (Ultralight to Black) with matching italics, plus the italic cut. Obtained from [developer.apple.com/fonts](https://developer.apple.com/fonts/).

### ✨ Scream Real
The 'Scream Real' font is a decorative/display typeface characterized by a bold and striking design with sharp, angular edges, giving it a dynamic and aggressive style.

### ✨ SF Mono
A clean and legible monospaced font.

### ✨ The Untold Story
A mysterious and intriguing font.

### ✨ Trobosh
A powerful and impactful font.

---

## 🚀 Installation

A cross-platform installer (`install_fonts.py`) is provided. It detects your OS and installs all fonts to the correct font directory. Python 3.6+ is required.

**Quick start:**

```bash
# Windows (double-click install_fonts.bat, or run:)
python install_fonts.py

# macOS / Linux
python3 install_fonts.py
```

**Options:**

```bash
python3 install_fonts.py --list      # list the fonts that would be installed
python3 install_fonts.py --dry-run   # preview actions without copying anything
python3 install_fonts.py --system    # install system-wide (needs sudo/admin)
python3 install_fonts.py --scope user # per-user install (default)
```

| OS | User install (default) | System install (`--system`) |
| --- | --- | --- |
| Windows | `%LOCALAPPDATA%\Microsoft\Windows\Fonts` + HKCU registry | `C:\Windows\Fonts` + HKLM registry |
| macOS | `~/Library/Fonts` | `/Library/Fonts` |
| Linux | `~/.local/share/fonts` + `fc-cache` | `/usr/share/fonts` + `fc-cache` |

**Notes:**

- On Windows, `install_fonts.bat` will run the Python installer automatically if Python is installed; otherwise it falls back to the legacy system-wide installer ( Administrator required).
- Existing fonts with the same filename are skipped, so the script can safely be re-run.
- On Linux, `fontconfig` (`fc-cache`) refreshes the font cache automatically when available.

---

## 🤝 Contributing

Feel free to contribute to this collection by adding new fonts. Please follow the existing directory structure and naming conventions.

1. Fork the repository.
2. Add your new font to the appropriate directory.
3. Update this `README.md` file to include the new font.
4. Create a pull request.

---

## 📜 License

The license for each font is located in its respective directory. Please review the license before using a font in a commercial project. If a font does not have a license, it is recommended to contact the font author for more information.