import typing

DEFAULT_POLL_INTERVAL: typing.Final[float] = 5.0

#: Default ADB swipe coordinates (x1, y1, x2, y2, duration_ms)
#: This simulates a swipe from bottom-center to top-center.
ADB_SWIPE_COMMAND: typing.Final[typing.List[str]] = [
    "adb",
    "shell",
    "input",
    "swipe",
    "500",  # x1
    "1500", # y1 (bottom)
    "500",  # x2
    "500",  # y2 (top)
    "100",  # duration (ms)
]
