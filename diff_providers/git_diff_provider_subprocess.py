from base.git_diff_provider_base import GitDiffProviderBase

import subprocess
import pathlib
import sys

import click

class GitDiffProviderSubprocess(GitDiffProviderBase):
    """
    Implementation of GitDiffProviderBase using subprocess to get git diffs.
    """

    def get_current_git_diff(self, repo_path: pathlib.Path) -> str:
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
        except subprocess.CalledProcessError as exception:
            # This error is usually harmless if the repo is empty or not yet fully initialized
            if exception.stderr.strip().startswith("fatal: not a git repository"):
                click.echo(
                    f"Hint: {repo_path} is not a valid git repository.",
                    err=True,
                )

                return "" # Treat as no diff

            click.echo(
                f"Error checking git diff: {exception.stderr.strip()}",
                err=True,
            )

            return ""  # Return an empty string to maintain return type consistency
        except Exception as exception:
            click.echo(f"An unexpected error occurred checking git: {exception}", err=True)
            return ""
