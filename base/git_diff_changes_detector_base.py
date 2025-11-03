import abc
import pathlib
import typing

class GitDiffChangesDetectorBase(abc.ABC):
    """
    Abstract base class for all git diff change detectors.

    Defines the contract for determining if a "rewardable" amount
    of new work has occurred since the last check.
    """

    def __init__(self, repo_path: pathlib.Path) -> None:
        """Initializes the detector with the repository path."""
        self.repo_path = repo_path
        self._last_state = self.get_current_state()

    @abc.abstractmethod
    def get_current_state(self) -> typing.Any:
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
