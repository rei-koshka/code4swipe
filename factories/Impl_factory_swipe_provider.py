from base.impl_factory_base import ImplFactoryBase
from base.swipe_provider_base import SwipeProviderBase
from constants.enums import SwipeProviders
from swipe_providers.swipe_provider_adb import SwipeProviderADB

import typing

class ImplFactorySwipeProvider(ImplFactoryBase[SwipeProviderBase, SwipeProviders]):
    """
    Factory for creating instances of SwipeProviderBase implementations.
    """

    def __init__(self, verbose: bool):
        self.verbose = verbose

    @property
    def impl_name_class(self) -> type[SwipeProviders]:
        return SwipeProviders

    def get_impl_map(self) -> typing.Dict[SwipeProviders, typing.Callable[[], SwipeProviderBase]]:
        """
        Returns a map of swipe provider names to their factory functions.
        """
        return {
            SwipeProviders.ADB: lambda: SwipeProviderADB(verbose=self.verbose),
        }
