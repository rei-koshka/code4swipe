from constants.constants import ADB_SWIPE_COMMAND
from base.swipe_provider_base import SwipeProviderBase

import subprocess

import click

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
            click.echo(f"Running check: {' '.join(adb_command)}", err=True)

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
        except subprocess.CalledProcessError as exception:
            click.echo(
                "Error: adb command failed. "
                "Is it installed and in your PATH?",
                err=True,
            )

            if self.verbose:
                click.echo(f"ADB Error (stderr): {exception.stderr.strip()}", err=True)

            return False
        except Exception as exception:
            click.echo(f"An unexpected error occurred checking ADB: {exception}", err=True)
            return False

    def swipe_up(self) -> None:
        """Executes the ADB swipe up command."""
        if self.verbose:
            click.echo(
                f"Running swipe: {' '.join(ADB_SWIPE_COMMAND)}",
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
        except subprocess.CalledProcessError as exception:
            click.echo(
                f"Error executing swipe: {exception.stderr.strip()}",
                err=True,
            )

            if self.verbose:
                click.echo(f"Swipe failed stdout: {exception.stdout.strip()}", err=True)

            click.echo(
                "Hint: Is your Android device connected and "
                "USB debugging enabled?",
                err=True,
            )
        except Exception as exception:
            click.echo(f"An unexpected error occurred during swipe: {exception}", err=True)
