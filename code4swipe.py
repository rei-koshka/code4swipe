#!/usr/bin/env python3

"""
code4swipe: A CLI tool to motivate coding by triggering a "swipe up"
(like in TikTok) via ADB when new git diff lines are detected.

This tool monitors a specified git repository. When it detects changes
based on a chosen strategy (e.g., increased line count), it executes
a swipe up command using a chosen provider.
"""

import abc
import os
import pathlib
import subprocess
import sys
import time
import typing

from enum import StrEnum

import click

# --- Enums / Constants ---

class SwipeProviders(StrEnum):
    """Defines available swipe provider choices."""
    ADB = "adb"

class ChangeDetectors(StrEnum):
    """Defines available change detector choices."""
    LINECOUNT = "linecount"
    EXACT = "exact"

DEFAULT_POLL_INTERVAL: typing.Final[float] = 5.0

#: Default ADB swipe coordinates (x1, y1, x2, y2, duration_ms)
#: This simulates a swipe from bottom-center to top-center.
ADB_SWIPE_COMMAND: typing.Final[typing.List[str]] = [
    "adb",
    "shell",
    "input",
    "swipe",
    "500",  # x1
    "1500", # y1 (bottom)
    "500",  # x2
    "500",  # y2 (top)
    "100",  # duration (ms)
]

# --- Git Helpers ---

def get_current_git_diff(repo_path: pathlib.Path) -> str:
    """
    Runs git diff and returns the entire output string.

    Args:
        repo_path: The path to the repository.

    Returns:
        The full output of git diff as a string.

    Raises:
        SystemExit: If git is not found or repo is invalid.
    """
    git_command = [
        "git",
        "-C",
        str(repo_path),
        "diff",
    ]

    try:
        result = subprocess.run(
            git_command,
            capture_output=True,
            check=True,
            text=True,
            encoding="utf-8",
        )

        return result.stdout
    except FileNotFoundError:
        click.echo(
            "Error: git command not found. "
            "Is it installed and in your PATH?",
            err=True,
        )

        sys.exit(1)  # Critical error, can not continue
    except subprocess.CalledProcessError as e:
        # This error is usually harmless if the repo is empty or not yet fully initialized
        if e.stderr.strip().startswith("fatal: not a git repository"):
            click.echo(
                f"Hint: {repo_path} is not a valid git repository.",
                err=True,
            )

            return "" # Treat as no diff

        click.echo(
            f"Error checking git diff: {e.stderr.strip()}",
            err=True,
        )

        return ""
    except Exception as e:
        click.echo(f"An unexpected error occurred checking git: {e}", err=True)
        return ""

# --- Strategy: Change Detection ---

class GitDiffChangesDetectorBase(abc.ABC):
    """
    Abstract base class for all git diff change detectors.

    Defines the contract for determining if a "rewardable" amount
    of new work has occurred since the last check.
    """

    def __init__(self, repo_path: pathlib.Path) -> None:
        """Initializes the detector with the repository path."""
        self.repo_path = repo_path
        self._last_state = self._get_current_state()

    @abc.abstractmethod
    def _get_current_state(self) -> typing.Any:
        """Calculates and returns the current state of the diff."""
        raise NotImplementedError

    @abc.abstractmethod
    def check_for_new_work(self) -> bool:
        """
        Checks for new work, updates the internal state, and returns True
        if a reward should be triggered.
        """
        raise NotImplementedError

    @property
    def initial_status_message(self) -> str:
        """Returns a string describing the initial state."""
        return f"Initial state: {self._last_state}. Waiting for new code..."


class GitDiffChangesDetectorLineCount(GitDiffChangesDetectorBase):
    """
    Detects new work by checking if the total number of lines in the
    git diff has increased.
    """

    def _get_current_state(self) -> int:
        """Returns the number of lines in the current git diff."""
        diff_string = get_current_git_diff(repo_path=self.repo_path)
        return len(diff_string.splitlines())

    def check_for_new_work(self) -> bool:
        """
        Triggers a reward if the current line count is GREATER THAN
        the last recorded count.
        """
        current_count = self._get_current_state()
        has_new_work = current_count > self._last_state

        # Always update the baseline to the current state.
        self._last_state = current_count

        return has_new_work

    @property
    def initial_status_message(self) -> str:
        """Returns a string describing the initial state (line count)."""
        return f"Initial diff lines: {self._last_state}. Waiting for new code..."


class GitDiffChangesDetectorExact(GitDiffChangesDetectorBase):
    """
    Detects new work by checking if the whole git diff string has changed
    (i.e., is not equal to the last recorded diff string).

    Note: This will trigger a reward on ANY change, including deletions.
    """

    def _get_current_state(self) -> str:
        """Returns the entire current git diff string."""
        return get_current_git_diff(repo_path=self.repo_path)

    def check_for_new_work(self) -> bool:
        """
        Triggers a reward if the current diff string is NOT EQUAL to
        the last recorded diff string.
        """
        current_diff = self._get_current_state()
        has_new_work = current_diff != self._last_state

        # Always update the baseline to the current state.
        self._last_state = current_diff

        return has_new_work

    @property
    def initial_status_message(self) -> str:
        """Returns a string describing the initial state (diff hash)."""
        # Using hash of the diff string for a compact status message
        diff_hash = hash(self._last_state)
        return f"Initial diff hash: {diff_hash}. Waiting for ANY change..."


# --- Strategy: Swipe Providers ---

class SwipeProviderBase(abc.ABC):
    """
    Abstract base class (interface) for all swipe providers.
    """

    def __init__(self, verbose: bool = False) -> None:
        """Initializes the provider."""
        self.verbose = verbose

    @abc.abstractmethod
    def swipe_up(self) -> None:
        """Executes the swipe up action."""
        raise NotImplementedError

    @abc.abstractmethod
    def check_availability(self) -> bool:
        """Checks if the provider is ready."""
        raise NotImplementedError


class SwipeProviderADB(SwipeProviderBase):
    """
    A swipe provider that uses the Android Debug Bridge (ADB).
    """

    def __init__(self, verbose: bool = False) -> None:
        """Initializes the ADB provider."""
        super().__init__(verbose=verbose)

    def check_availability(self) -> bool:
        """Checks if the adb command is available."""
        adb_command = [
            "adb",
            "version",
        ]

        if self.verbose:
            click.echo(f"Running check: {" ".join(adb_command)}", err=True)

        try:
            result = subprocess.run(
                adb_command,
                capture_output=True,
                check=True,
                text=True,
            )

            if self.verbose:
                # Log first line of version output
                log_line = result.stdout.splitlines()[0] if result.stdout else "OK"
                click.echo(f"ADB check OK: {log_line}", err=True)

            return True
        except FileNotFoundError:
            click.echo(
                "Error: adb command not found. "
                "Is it installed and in your PATH?",
                err=True,
            )

            return False
        except subprocess.CalledProcessError as e:
            click.echo(
                "Error: adb command failed. "
                "Is it installed and in your PATH?",
                err=True,
            )

            if self.verbose:
                click.echo(f"ADB Error (stderr): {e.stderr.strip()}", err=True)

            return False
        except Exception as e:
            click.echo(f"An unexpected error occurred checking ADB: {e}", err=True)
            return False

    def swipe_up(self) -> None:
        """Executes the ADB swipe up command."""
        if self.verbose:
            click.echo(
                f"Running swipe: {" ".join(ADB_SWIPE_COMMAND)}",
                err=True,
            )

        try:
            result = subprocess.run(
                ADB_SWIPE_COMMAND,
                check=True,
                capture_output=True,
                text=True,
            )
            if self.verbose:
                click.echo("Swipe command executed successfully.", err=True)

                if result.stdout:
                    click.echo(f"Swipe stdout: {result.stdout.strip()}", err=True)

                if result.stderr:
                    click.echo(f"Swipe stderr: {result.stderr.strip()}", err=True)

        except FileNotFoundError:
            click.echo(
                "Error: adb command not found. "
                "Please ensure it is installed and in your PATH.",
                err=True,
            )
        except subprocess.CalledProcessError as e:
            click.echo(
                f"Error executing swipe: {e.stderr.strip()}",
                err=True,
            )

            if self.verbose:
                click.echo(f"Swipe failed stdout: {e.stdout.strip()}", err=True)

            click.echo(
                "Hint: Is your Android device connected and "
                "USB debugging enabled?",
                err=True,
            )
        except Exception as e:
            click.echo(f"An unexpected error occurred during swipe: {e}", err=True)


# --- Factory Functions ---

def get_swipe_provider(
    provider_name: str,
    verbose: bool,
) -> SwipeProviderBase:
    """Factory to get an instance of a swipe provider."""
    provider_map: typing.Dict[StrEnum, typing.Type[SwipeProviderBase]] = {
        SwipeProviders.ADB: SwipeProviderADB,
    }

    provider_class = provider_map.get(SwipeProviders(provider_name))

    if not provider_class:
        click.echo(
            f"Error: Unknown provider {provider_name}. "
            f"Available: {list(SwipeProviders)}",
            err=True,
        )

        raise click.Abort()

    provider_instance = provider_class(verbose=verbose)

    if not provider_instance.check_availability():
        click.echo(
            f"Error: Provider {provider_name} failed availability check.",
            err=True,
        )

        raise click.Abort()

    return provider_instance


def get_changes_detector(
    detector_name: str,
    repo_path: pathlib.Path,
) -> GitDiffChangesDetectorBase:
    """Factory to get an instance of a changes detector."""
    detector_map: typing.Dict[StrEnum, typing.Type[GitDiffChangesDetectorBase]] = {
        ChangeDetectors.LINECOUNT: GitDiffChangesDetectorLineCount,
        ChangeDetectors.EXACT: GitDiffChangesDetectorExact,
    }

    detector_class = detector_map.get(ChangeDetectors(detector_name.lower()))

    if not detector_class:
        click.echo(
            f"Error: Unknown detector {detector_name}. "
            f"Available: {list(ChangeDetectors)}",
            err=True,
        )

        raise click.Abort()

    return detector_class(repo_path=repo_path)


# --- CLI Interface ---

@click.command(
    context_settings=dict(
        help_option_names=[
            "-h",
            "--help",
        ],
    ),
)
@click.option(
    "--repo",
    "repo_path",
    type=click.Path(
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        path_type=pathlib.Path,
    ),
    default=lambda: pathlib.Path(os.getcwd()),
    show_default="current working directory",
    help="Path to the git repository to monitor.",
)
@click.option(
    "--provider",
    "provider_name",
    type=click.Choice(
        list(SwipeProviders),
        case_sensitive=False,
    ),
    default=SwipeProviders.ADB,
    show_default=True,
    help="The swipe provider to use.",
)
@click.option(
    "--changes",
    "detector_name",
    type=click.Choice(
        list(ChangeDetectors),
        case_sensitive=False,
    ),
    default=ChangeDetectors.EXACT.value,
    show_default=True,
    help="The strategy to detect new code changes.",
)
@click.option(
    "--poll-interval",
    "poll_interval",
    type=click.FLOAT,
    default=DEFAULT_POLL_INTERVAL,
    show_default=True,
    help="The interval in seconds to check the git repository for changes.",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    default=False,
    help="Enable verbose logging for provider actions.",
)
def main(
    repo_path: pathlib.Path,
    provider_name: str,
    detector_name: str,
    poll_interval: float,
    verbose: bool,
) -> None:
    """
    Monitors a git repo for changes and triggers a "swipe up"
    via a provider (e.g., ADB) to reward you for coding.

    This is a "Dopamine CLI" for coders! 🚀
    """

    # Check for Python version compatibility
    if sys.version_info < (3, 11):
        click.echo(
            "Warning: StrEnum (used in this script) requires Python 3.11 or higher. "
            "Please upgrade or replace StrEnum with standard Enum and string mapping "
            "if you encounter issues.",
            err=True,
        )

    if verbose:
        click.echo("Verbose mode enabled.", err=True)

    try:
        # Initialize Provider
        provider = get_swipe_provider(
            provider_name=provider_name,
            verbose=verbose,
        )

        # Initialize Detector
        detector = get_changes_detector(
            detector_name=detector_name,
            repo_path=repo_path,
        )
    except click.Abort:
        click.echo("Failed to initialize. Exiting.", err=True)
        sys.exit(1)

    click.echo("---")
    click.echo(f"Monitoring git diff in: `{detector.repo_path}` using `{detector_name}` strategy.")
    click.echo(detector.initial_status_message)
    click.echo(f"Polling interval: {poll_interval} seconds.")
    click.echo("🚀 code4swipe is running! Start writing code.")
    click.echo("Press CTRL+C to exit.")

    try:
        while True:
            if detector.check_for_new_work():
                click.echo(
                    f"[{time.strftime("%H:%M:%S")}] "
                    "New code detected! Swiping for dopamine... 📱"
                )

                provider.swipe_up()

            time.sleep(poll_interval)

    except KeyboardInterrupt:
        click.echo("\n👋 Exiting. Happy coding!")
        sys.exit(0)


if __name__ == "__main__":
    main()
