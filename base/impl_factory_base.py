import abc
import typing

from enum import StrEnum

import click

TBaseClass = typing.TypeVar("TBaseClass", bound=abc.ABC)
TImplName = typing.TypeVar("TImplName", bound=StrEnum)

class ImplFactoryBase(abc.ABC, typing.Generic[TBaseClass, TImplName]):
    """
    Base class for implementation factories.
    """

    @property
    @abc.abstractmethod
    def impl_name_class(self) -> type[TImplName]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_impl_map(self) -> typing.Dict[TImplName, typing.Callable[[], TBaseClass]]:
        """
        Returns a map of implementation names to their factory functions.
        """
        raise NotImplementedError

    def get_impl_instance(self, impl_name_str: str) -> TBaseClass:
        """
        Gets an instance of the implementation based on the provided name.

        Args:
            impl_name: The name of the implementation to retrieve.

        Returns:
            An instance of the implementation.

        Raises:
            click.Abort: If the implementation name is not found.
        """
        impl_map = self.get_impl_map()

        impl_name = self.impl_name_class(impl_name_str.lower())

        instance_factory = impl_map.get(impl_name)

        if not instance_factory:
            click.echo(
                f"Error: Unknown implementation {impl_name}. "
                f"Available: {self.get_instance_names_list()}",
                err=True,
            )

            raise click.Abort()

        return instance_factory()

    def get_instance_names_list(self) -> typing.List[str]:
        """
        Returns a list of available implementation names.
        """
        return [name.value for name in self.get_impl_map().keys()]
