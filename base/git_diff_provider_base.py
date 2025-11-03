import abc
import pathlib

class GitDiffProviderBase(abc.ABC):
    """
    Abstract base class for providing git diffs.
    """

    @abc.abstractmethod
    def get_current_git_diff(self, repo_path: pathlib.Path) -> str:
        """
        Runs git diff and returns the entire output string.

        Args:
            repo_path: The path to the repository.

        Returns:
            The full output of git diff as a string.
        """
        raise NotImplementedError
