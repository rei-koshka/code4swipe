import typing
import click
import pathlib

from base.swipe_provider_base import SwipeProviderBase
from base.git_diff_changes_detector_base import GitDiffChangesDetectorBase
from change_detectors.git_diff_changes_detector_exact import GitDiffChangesDetectorExact
from change_detectors.git_diff_changes_detector_line_count import GitDiffChangesDetectorLineCount
from constants.enums import SwipeProviders, ChangeDetectors
from swipe_providers.swipe_provider_adb import SwipeProviderADB

def get_swipe_provider(
    provider_name: str,
    verbose: bool,
) -> SwipeProviderBase:
    """Factory to get an instance of a swipe provider."""
    provider_map: typing.Dict[SwipeProviders, typing.Type[SwipeProviderBase]] = {
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
    detector_map: typing.Dict[ChangeDetectors, typing.Type[GitDiffChangesDetectorBase]] = {
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
