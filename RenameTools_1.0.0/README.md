# Android Resource Batch Renaming Tool

## Project Overview

This project aims to provide a one-stop batch renaming solution for Android project resources, suitable for scenarios where multiple channel packages (i.e., different resource names generated from the same codebase) need to be produced. With this tool, you can greatly improve the efficiency of resource renaming, reduce manual errors, and quickly generate multi-channel Android applications.

## Background

In actual Android project development, especially when multiple channel packages (such as different brands or channels generated from the same codebase) need to be produced, it is often necessary to batch rename resource files (such as strings, drawable, layout, etc.) to avoid resource conflicts between packages or to achieve customization. Manual renaming is tedious and error-prone, so this tool was developed to automate batch renaming of resources and synchronize reference updates.

## Features

- **Visual Operation Interface**: Based on Tkinter, supports directory selection, multi-package selection, renaming mode switching, etc.
- **Multi-Package Support**: Automatically scans all packages containing `AndroidManifest.xml` under the project root directory, supporting simultaneous processing of multiple packages.
- **Multiple Resource Types Supported**: Supports batch renaming of `strings`, `drawable`, `layout`, and other resources.
- **Flexible Renaming Modes**: Customizable prefix, supports "initial letter mode" and "full name mode".
- **Intelligent Uniqueness Handling**: Automatically avoids renaming conflicts to ensure the uniqueness of new resource names.
- **Reference Synchronization**: Automatically updates resource references in Java/Kotlin/XML/Manifest files, and supports DataBinding class name synchronization.
- **Log Output**: Real-time display of operation logs for easy tracking and troubleshooting.
- **Multithreading**: Smooth operation without UI freezing.

## Usage

### 1. Run the Source Code Directly

#### Environment Preparation

- Python 3.x
- Dependencies: `tkinter` (comes with the standard library), `xml`, `threading`, etc.

#### Startup

```bash
cd source
python rename_Tools_2.0.0.py
```

### 2. Use the PyInstaller Packaged App

This project has been packaged as a Mac application (`rename_Tools.app`) via PyInstaller, which can be run directly without a Python environment.

#### Packaging Command Reference

If you need to package it yourself, refer to the following command:

```bash
pyinstaller --onefile --windowed -i popCorn.icns rename_Tools_2.0.0.py
```

- `--onefile`: Package as a single executable file
- `--windowed`: No command line window (suitable for GUI applications)
- `-i`: Specify application icon

### 3. Operation Process

1. **Select Project Root Directory**: Should contain the Android project root directory with all packages (such as app, gp, huawei, etc.).
2. **Select Packages**: Multiple selection supported, app package is selected by default.
3. **Set Renaming Mode**: Enter prefix, and choose whether to enable "initial letter mode".
4. **Click "Start Renaming"**: The tool will automatically complete resource renaming and reference updates.
5. **View Log Output**: The operation process and results will be displayed in real time in the log area.

## Notes

- It is recommended to back up your project before operation to avoid resource loss due to misoperation.
- Only standard Android project structures are supported (i.e., the `src/main/res` directory structure).
- Supports common resource directories such as multi-language values directories and different resolution drawable directories.

## Applicable Scenarios

- Android projects that need to generate multiple channel packages in batches
- Multi-package projects that need to standardize resource naming and avoid resource conflicts
- Development teams that need to automate resource and reference synchronization

## Contact & Feedback

If you have any questions or suggestions, feel free to submit an issue or contact us by email. 