# `code4swipe`: The Dopamine CLI for Coders

`code4swipe` is a command-line interface (CLI) tool that gamifies your coding process by rewarding you with an automatic "swipe up" action (like the satisfying gesture on TikTok or other social media feeds) whenever you introduce new changes to your local git repository.

It monitors your current working directory's `git diff` and triggers a **swipe** via a chosen provider (currently, **ADB** for Android devices) to give you a quick, satisfying break or a virtual "pat on the back" for your new lines of code.

## Features

- **Git Diff Monitoring:** Continuously monitors your local repository's uncommitted changes.
- **Two Detection Strategies:**
  - **`exact` (Default):** Triggers on **ANY** change to the git diff (additions, deletions, modifications).
  - **`linecount`:** Triggers only if the total number of lines in the git diff has **increased** since the last check (focused on rewarding additions).
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

You can install `code4swipe` either globally for easy access or within a Python Virtual Environment (`.venv`) for isolated usage.

### 1\. Global Installation (Recommended for quick use)

The script depends on the `click` package for its CLI functionality.

```bash
# Install the required package
pip install click
```

For a global installation, copy the script file (let's assume you save it as `code4swipe.py`) and make it executable.

1. **Save the script:**

   ```bash
   # Save the script contents to a file
   wget -O code4swipe.py https://raw.githubusercontent.com/Danand/code4swipe/refs/heads/main/code4swipe.md
   # OR
   # Create the file and paste the content
   ```

2. **Make it executable:**

   ```bash
   chmod +x code4swipe.py
   ```

3. **Move to a PATH directory:**

   ```bash
   # For Linux/macOS
   sudo mv code4swipe.py /usr/local/bin/code4swipe
   # For Windows, you'd place it in a directory listed in your PATH and rename
   # it, or call it directly with `python code4swipe.py`.
   ```

Now you can run it from any directory using the command `code4swipe`.

### 3\. Virtual Environment (`.venv`) Installation

Using a virtual environment is the recommended way to manage Python dependencies for development.

1. **Create and activate the environment:**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
   ```

2. **Install requirements:**

   ```bash
   pip install click
   ```

3. **Save the script:** Save the script contents as `code4swipe.py` inside your project directory.

4. **Run the script:**

    ```bash
    python code4swipe.py
    ```

    *(You'll need to run this command from the directory containing `code4swipe.py` or specify the full path.)*

-----

## Usage

Run the tool from within the git repository you want to monitor.

### Basic Usage

The simplest way to run `code4swipe` is from the root of your git repository.

```bash
code4swipe
# OR if using venv:
python code4swipe.py
```

This will:

- Monitor the current directory (`--repo .`).
- Use the `adb` provider (`--provider adb`).
- Use the `exact` change detection strategy (`--changes exact`).
- Check for changes every 5 seconds (`--poll-interval 5.0`).

### Options

| Option | Shorthand | Default | Description |
| :--- | :--- | :--- | :--- |
| `--repo` | | `cwd` | Path to the git repository to monitor. |
| `--provider` | | `adb` | The swipe provider to use. (Currently, only **`adb`** is supported). |
| `--changes` | | `exact` | The strategy to detect new code changes. Choices: **`exact`** or **`linecount`**. |
| `--poll-interval` | | `5.0` | The interval in seconds to check the git repository for changes. |
| `--verbose` | `-v` | `False` | Enable verbose logging for provider actions (useful for debugging ADB issues). |

### Examples

#### 1\. Reward only for code additions (linecount strategy)

```bash
code4swipe --changes linecount
```

#### 2\. Monitor a different repository with a longer interval

```bash
code4swipe --repo /path/to/my/other/project --poll-interval 10
```

#### 3\. Debug ADB connection issues

```bash
code4swipe --verbose
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
3. **Check the strategy:** If using `--changes linecount`, ensure your new code *increases* the total line count of the diff (i.e., you haven't just deleted lines).
