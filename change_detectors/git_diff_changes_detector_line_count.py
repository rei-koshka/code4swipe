from base.git_diff_changes_detector_base import GitDiffChangesDetectorBase
from diff_providers.git_diff_provider_subprocess import GitDiffProviderSubprocess

class GitDiffChangesDetectorLineCount(GitDiffChangesDetectorBase):
    """
    Detects new work by checking if the total number of lines in the
    git diff has increased.
    """

    def get_current_state(self) -> int:
        """Returns the number of lines in the current git diff."""
        diff_provider = GitDiffProviderSubprocess()
        diff_string = diff_provider.get_current_git_diff(repo_path=self.repo_path)

        return len(diff_string.splitlines())

    def check_for_new_work(self) -> bool:
        """
        Triggers a reward if the current line count is GREATER THAN
        the last recorded count.
        """
        current_count = self.get_current_state()
        has_new_work = current_count != self._last_state

        # Always update the baseline to the current state.
        self._last_state = current_count

        return has_new_work

    @property
    def initial_status_message(self) -> str:
        """Returns a string describing the initial state (line count)."""
        return f"Initial diff lines: {self._last_state}. Waiting for new code..."
