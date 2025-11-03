from enum import StrEnum

class SwipeProviders(StrEnum):
    """Defines available swipe provider choices."""
    ADB = "adb"

class ChangeDetectors(StrEnum):
    """Defines available change detector choices."""
    LINECOUNT = "linecount"
    EXACT = "exact"
