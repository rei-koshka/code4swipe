from base.git_diff_changes_detector_base import GitDiffChangesDetectorBase
from diff_providers.git_diff_provider_subprocess import GitDiffProviderSubprocess

class GitDiffChangesDetectorExact(GitDiffChangesDetectorBase):
    """
    Detects new work by checking if the whole git diff string has changed
    (i.e., is not equal to the last recorded diff string).

    Note: This will trigger a reward on ANY change, including deletions.
    """

    def get_current_state(self) -> str:
        """Returns the entire current git diff string."""
        diff_provider = GitDiffProviderSubprocess()
        return diff_provider.get_current_git_diff(repo_path=self.repo_path)

    def check_for_new_work(self) -> bool:
        """
        Triggers a reward if the current diff string is NOT EQUAL to
        the last recorded diff string.
        """
        current_diff = self.get_current_state()
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
