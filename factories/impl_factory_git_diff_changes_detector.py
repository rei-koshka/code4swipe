
from base.git_diff_changes_detector_base import GitDiffChangesDetectorBase
from base.impl_factory_base import ImplFactoryBase
from constants.enums import ChangeDetectors
from change_detectors.git_diff_changes_detector_line_count import GitDiffChangesDetectorLineCount
from change_detectors.git_diff_changes_detector_exact import GitDiffChangesDetectorExact

import typing
import pathlib

class ImplFactoryGitDiffChangesDetector(ImplFactoryBase[GitDiffChangesDetectorBase, ChangeDetectors]):
    """
    Factory for creating instances of GitDiffChangesDetectorBase implementations.
    """

    def __init__(self, repo_path: pathlib.Path):
        self.repo_path = repo_path

    @property
    def impl_name_class(self) -> type[ChangeDetectors]:
        return ChangeDetectors

    def get_impl_map(self) -> typing.Dict[ChangeDetectors, typing.Callable[[], GitDiffChangesDetectorBase]]:
        """
        Returns a map of change detector names to their factory functions.
        """
        return {
            ChangeDetectors.LINECOUNT: lambda: GitDiffChangesDetectorLineCount(repo_path=self.repo_path),
            ChangeDetectors.EXACT: lambda: GitDiffChangesDetectorExact(repo_path=self.repo_path),
        }
