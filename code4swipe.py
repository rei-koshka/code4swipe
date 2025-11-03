#!/usr/bin/env python3

"""
code4swipe: A CLI tool to motivate coding by triggering a "swipe up"
(like in TikTok) via ADB when new git diff lines are detected.

This tool monitors a specified git repository. When it detects changes
based on a chosen strategy (e.g., increased line count), it executes
a swipe up command using a chosen provider.
"""

from constants.constants import DEFAULT_POLL_INTERVAL
from constants.enums import ChangeDetectors, SwipeProviders
from factories.Impl_factory_swipe_provider import ImplFactorySwipeProvider
from factories.impl_factory_git_diff_changes_detector import ImplFactoryGitDiffChangesDetector

import os
import pathlib
import sys
import time

import click


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
        # Initialize Swipe Provider
        provider_factory = ImplFactorySwipeProvider(verbose=verbose)
        provider = provider_factory.get_impl_instance(provider_name)

        # Initialize Git Diff Detector
        detector_factory = ImplFactoryGitDiffChangesDetector(repo_path=repo_path)
        detector = detector_factory.get_impl_instance(detector_name)
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
                provider.swipe_up()

                click.echo(
                    f"[{time.strftime("%H:%M:%S")}] "
                    "New code detected! Swiping for dopamine... 📱"
                )

            time.sleep(poll_interval)

    except KeyboardInterrupt:
        click.echo("\n👋 Exiting. Happy coding!")
        sys.exit(0)


if __name__ == "__main__":
    main()
