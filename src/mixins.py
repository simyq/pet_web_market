"""Module for mixin classes (for logging to console, log-files), storing, etc."""


class MixinConsoleLog:
    """Mixin class for console-logging, when creating a new object"""

    def __init__(self: object) -> None:
        print(repr(self))
