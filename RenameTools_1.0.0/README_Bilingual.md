# Android 资源批量重命名工具  
# Android Resource Batch Renaming Tool

## 项目简介  
## Project Overview

本项目旨在为 Android 项目提供一站式的资源批量重命名解决方案，适用于需要生成多渠道包（即同一套代码产出多个不同资源名的应用）的场景。通过本工具，可以极大提升资源重命名的效率，减少人工操作失误，助力快速产出多渠道的 Android 应用。

This project aims to provide a one-stop batch renaming solution for Android project resources, suitable for scenarios where multiple channel packages (i.e., different resource names generated from the same codebase) need to be produced. With this tool, you can greatly improve the efficiency of resource renaming, reduce manual errors, and quickly generate multi-channel Android applications.

## 诞生背景  
## Background

在实际 Android 项目开发中，尤其是需要产出多个渠道包（如同一套代码生成不同品牌、渠道的应用）时，往往需要对资源文件（如 strings、drawable、layout 等）进行批量重命名，以避免包体间资源冲突或实现定制化。手动重命名不仅繁琐且易出错，因此开发了本工具，实现资源的自动化批量重命名和引用同步更新。

In actual Android project development, especially when multiple channel packages (such as different brands or channels generated from the same codebase) need to be produced, it is often necessary to batch rename resource files (such as strings, drawable, layout, etc.) to avoid resource conflicts between packages or to achieve customization. Manual renaming is tedious and error-prone, so this tool was developed to automate batch renaming of resources and synchronize reference updates.

## 功能特性  
## Features

- **可视化操作界面**：基于 Tkinter 实现，支持目录选择、包体多选、重命名模式切换等。
- **多包体支持**：自动扫描项目根目录下所有含有 `AndroidManifest.xml` 的包体，支持多包体同时处理。
- **多资源类型支持**：支持对 `strings`、`drawable`、`layout` 等资源的批量重命名。
- **重命名模式灵活**：可自定义前缀，支持"首字母模式"与"全名模式"。
- **智能唯一性处理**：自动避免重命名冲突，确保新资源名唯一。
- **引用同步更新**：自动更新 Java/Kotlin/XML/Manifest 文件中的资源引用，支持 DataBinding 类名同步替换。
- **日志输出**：实时显示操作日志，便于追踪和排查问题。
- **多线程处理**：界面不卡顿，操作流畅。

- **Visual Operation Interface**: Based on Tkinter, supports directory selection, multi-package selection, renaming mode switching, etc.
- **Multi-Package Support**: Automatically scans all packages containing `AndroidManifest.xml` under the project root directory, supporting simultaneous processing of multiple packages.
- **Multiple Resource Types Supported**: Supports batch renaming of `strings`, `drawable`, `layout`, and other resources.
- **Flexible Renaming Modes**: Customizable prefix, supports "initial letter mode" and "full name mode".
- **Intelligent Uniqueness Handling**: Automatically avoids renaming conflicts to ensure the uniqueness of new resource names.
- **Reference Synchronization**: Automatically updates resource references in Java/Kotlin/XML/Manifest files, and supports DataBinding class name synchronization.
- **Log Output**: Real-time display of operation logs for easy tracking and troubleshooting.
- **Multithreading**: Smooth operation without UI freezing.

## 使用方法  
## Usage

### 1. 直接运行源码  
### 1. Run the Source Code Directly

#### 环境准备  
#### Environment Preparation

- Python 3.x
- 依赖库：`tkinter`（标准库自带）、`xml`、`threading` 等

- Python 3.x
- Dependencies: `tkinter` (comes with the standard library), `xml`, `threading`, etc.

#### 启动方式  
#### Startup

```bash
cd source
python rename_Tools_2.0.0.py
```

### 2. 使用 PyInstaller 封装的 App  
### 2. Use the PyInstaller Packaged App

本项目已通过 PyInstaller 封装为 Mac 应用（`rename_Tools.app`），可直接双击运行，无需 Python 环境。

This project has been packaged as a Mac application (`rename_Tools.app`) via PyInstaller, which can be run directly without a Python environment.

#### 打包命令参考  
#### Packaging Command Reference

如需自行打包，可参考如下命令：

If you need to package it yourself, refer to the following command:

```bash
pyinstaller --onefile --windowed -i popCorn.icns rename_Tools_2.0.0.py
```

- `--onefile`：打包为单一可执行文件
- `--windowed`：无命令行窗口（适合 GUI 应用）
- `-i`：指定应用图标

- `--onefile`: Package as a single executable file
- `--windowed`: No command line window (suitable for GUI applications)
- `-i`: Specify application icon

### 3. 操作流程  
### 3. Operation Process

1. **选择项目根目录**：需包含各包体（如 app、gp、huawei 等）的 Android 项目根目录。
2. **选择包体**：可多选，默认勾选 app 包体。
3. **设置重命名模式**：输入前缀，可选择是否启用"首字母模式"。
4. **点击"开始重命名"**：工具将自动完成资源重命名及引用更新。
5. **查看日志输出**：操作过程及结果会实时显示在日志区。

1. **Select Project Root Directory**: Should contain the Android project root directory with all packages (such as app, gp, huawei, etc.).
2. **Select Packages**: Multiple selection supported, app package is selected by default.
3. **Set Renaming Mode**: Enter prefix, and choose whether to enable "initial letter mode".
4. **Click "Start Renaming"**: The tool will automatically complete resource renaming and reference updates.
5. **View Log Output**: The operation process and results will be displayed in real time in the log area.

## 注意事项  
## Notes

- 建议在操作前备份项目，避免误操作导致资源丢失。
- 仅支持标准 Android 项目结构（即 `src/main/res` 目录结构）。
- 支持多语言 values 目录、不同分辨率 drawable 目录等常见资源目录。

- It is recommended to back up your project before operation to avoid resource loss due to misoperation.
- Only standard Android project structures are supported (i.e., the `src/main/res` directory structure).
- Supports common resource directories such as multi-language values directories and different resolution drawable directories.

## 适用场景  
## Applicable Scenarios

- 需要批量生成多渠道包的 Android 项目
- 需要统一资源命名规范、避免资源冲突的多包体项目
- 需要自动化处理资源及引用同步的开发团队

- Android projects that need to generate multiple channel packages in batches
- Multi-package projects that need to standardize resource naming and avoid resource conflicts
- Development teams that need to automate resource and reference synchronization

## 联系与反馈  
## Contact & Feedback

如有问题或建议，欢迎通过 Issue 或邮件反馈。

If you have any questions or suggestions, feel free to submit an issue or contact us by email. 