# SmartStitch - Project Overview

## What is SmartStitch?
A Python application for stitching and cutting webtoons/manhwa/manhua raws. Uses pixel comparison to intelligently avoid cutting through SFX, speech bubbles, or drawings.

## Tech Stack
- **Language**: Python 3.10+
- **Package Manager**: Pipenv
- **GUI Framework**: PySide6 (Qt6)
- **Image Processing**: Pillow, NumPy, psd-tools
- **Build Tool**: PyInstaller

## Project Structure

```
SmartStitch/
├── SmartStitchGUI.py      # GUI entry point
├── SmartStitchConsole.py  # Console entry point
├── Pipfile                # Dependencies and scripts
├── setup.py               # Setup script for Mac/Linux
├── Build.spec             # PyInstaller spec (with icon)
├── BuildNoIcon.spec       # PyInstaller spec (no icon)
│
├── core/                  # Core logic (shared by GUI & Console)
│   ├── detectors/         # Slice location detection algorithms
│   │   ├── direct_slicing.py
│   │   ├── pixel_comparison.py
│   │   └── selector.py
│   ├── models/            # Data models
│   │   ├── app_profiles.py
│   │   ├── app_settings.py
│   │   └── work_directory.py
│   ├── services/          # Business logic services
│   │   ├── directory_explorer.py
│   │   ├── global_logger.py
│   │   ├── global_tracker.py
│   │   ├── image_handler.py
│   │   ├── image_manipulator.py
│   │   ├── postprocess_runner.py
│   │   └── settings_handler.py
│   └── utils/             # Utilities
│       ├── constants.py
│       ├── errors.py
│       └── funcs.py
│
├── gui/                   # GUI application
│   ├── controller.py
│   ├── launcher.py
│   ├── layout.ui          # Qt UI definition
│   ├── process.py
│   └── stylesheet.py
│
├── console/               # Console/CLI application
│   ├── launcher.py
│   └── process.py
│
├── scripts/               # Dev scripts
│   └── formatter.py
│
└── assets/                # Images, icons, etc.
```

## Key Commands (via Pipenv)
```bash
pipenv run gui          # Launch GUI
pipenv run console      # Launch console version
pipenv run build        # Build GUI with icon (Windows)
pipenv run build-no-icon  # Build GUI without icon (Mac/Linux)
pipenv run format       # Run code formatter
pipenv install          # Install all dependencies
```

## Python Version Management (Optional)
If you need to install Python 3.10+, you can use [uv](https://docs.astral.sh/uv/getting-started/installation/) as a Python version manager:
```bash
uv python install 3.10
```

## Dependencies
- **Runtime**: pillow, numpy, natsort, pyside6, pyqtdarktheme, psd-tools
- **Dev**: flake8, black, isort, pyinstaller

## Architecture Notes
- `core/` contains shared logic used by both GUI and console versions
- Two detector types: `pixel_comparison` (smart) and `direct_slicing` (exact cuts)
- Settings profiles supported for different projects/resolutions
- Logging system writes daily logs to `__logs__` folder
- Supports batch mode for processing multiple chapter folders
