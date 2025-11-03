# `code4swipe`: The Dopamine CLI for Coders

`code4swipe` is a CLI tool that gamifies your coding process by rewarding you with an automatic "swipe up" action (like the satisfying gesture on TikTok or other social media feeds) whenever you introduce new changes to your local git repository.

It monitors your current working directory's `git diff` and triggers a **swipe** via a chosen provider (currently, **ADB** for Android devices) to give you a quick, satisfying break or a virtual "pat on the back" for your new lines of code.

## Features

- **Git Diff Monitoring:** Continuously monitors your local repository's uncommitted changes.
- **Two Detection Strategies:**
  - **`exact` (Default):** Triggers on **ANY** change to the git diff (additions, deletions, modifications).
  - **`linecount`:** Triggers only if the total number of lines in the git diff has changed.
- **ADB Swipe Provider:** Uses the **Android Debug Bridge (ADB)** to execute a simulated "swipe up" on a connectedAndroid device.
- **Customizable:** Set your preferred repository path and polling interval.

-----

## Prerequisites

Before installation, ensure you have the following ready:

1. **Python 3.11+:** This script uses `StrEnum`, which requires Python 3.11 or newer.
2. **Git:** Must be installed and available in your system's PATH.
3. **ADB (Android Debug Bridge):** Required if you use the default `adb` provider.
   - ADB must be installed (usually part of the Android SDK Platform Tools) and accessible in your system's PATH.
   - Your Android device must be connected, with **USB Debugging** enabled.

-----

## Installation

### Install Globally

To install `code4swipe`, use the following command:

```bash
pip install code4swipe
```

This will install the package and its dependencies, making the `code4swipe` command available globally.

### Install in Virtual Environment

Using a virtual environment is the recommended way to manage Python dependencies for development.

1. Clone and `cd` in repo.

2. **Create and activate the environment:**

   ```bash
   python3.11 -m venv .venv
   source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
   ```

3. **Install requirements:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Make script executable:**

   ```bash
   chmod +x code4swipe.py
   ```

-----

## Usage

Run the tool from within the git repository you want to monitor.

### Basic Usage

The simplest way to run `code4swipe` is from the root of your git repository.

If installed **globally**:

```bash
python3 -m code4swipe
```

If installed in **virtual environment**:

```bash
./code4swipe.py --repo /path/to/my/other/project
```

### Options

| Option | Shorthand | Default | Description |
| :--- | :--- | :--- | :--- |
| `--repo` | | `cwd` | Path to the git repository to monitor. |
| `--provider` | | `adb` | The swipe provider to use. (Currently, only **`adb`** is supported). |
| `--changes` | | `exact` | The strategy to detect new code changes. Choices: **`exact`** or **`linecount`**. |
| `--poll-interval` | | `5.0` | The interval in seconds to check the git repository for changes. |
| `--verbose` | `-v` | `False` | Enable verbose logging for provider actions (useful for debugging ADB issues). |

### Examples

#### Reward only for code additions (linecount strategy)

```bash
python3 -m code4swipe --changes linecount
```

#### Monitor a different repository with a longer interval

```bash
python3 -m code4swipe --repo /path/to/my/other/project --poll-interval 10
```

#### Debug ADB connection issues

```bash
python3 -m code4swipe --verbose
```

-----

## Troubleshooting

### `Error: adb command not found.`

Ensure **ADB (Android Debug Bridge)** is installed on your system and the directory containing the `adb` executable is added to your system's **PATH** environment variable.

### `Error: Provider adb failed availability check.`

This usually means ADB is installed but:

1. Your Android device is not connected.
2. USB debugging is not enabled on the device.
3. You haven't accepted the ADB connection prompt on your device.

Run the script with the verbose flag (`-v`) for more diagnostic information: `code4swipe -v`.

### `Warning: StrEnum (used in this script) requires Python 3.11 or higher...`

If you see this warning, your Python version is too old. You must upgrade to **Python 3.11 or newer** to run this script as-is.

### Script doesn't trigger a swipe

1. **Check your device:** Make sure the Android device is unlocked and the screen is on, ready to receive input.
2. **Check the git diff:** The script only reacts to uncommitted changes. Try making a small change to a file in the monitored repo. Run `git diff` manually to confirm you have changes.
3. **Check the strategy:** If using `--changes linecount`, ensure your new code changes the total line count of the diff.
