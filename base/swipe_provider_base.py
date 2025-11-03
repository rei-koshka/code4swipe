import abc

class SwipeProviderBase(abc.ABC):
    """
    Abstract base class for all swipe providers.
    """

    def __init__(self, verbose: bool = False) -> None:
        """Initializes the provider."""
        self.verbose = verbose

    @abc.abstractmethod
    def swipe_up(self) -> None:
        """Executes the swipe up action."""
        raise NotImplementedError

    @abc.abstractmethod
    def check_availability(self) -> bool:
        """Checks if the provider is ready."""
        raise NotImplementedError
