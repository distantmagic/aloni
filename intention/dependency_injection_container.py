import inspect
from typing import (
    Annotated,
    Generator,
    Sequence,
    Tuple,
    Type,
    get_args,
    get_origin,
)

from .role.get_root_class import get_root_class
from .role.role import Role
from .role.service import service
from .role.service_provider_wrapped import service_provider_wrapped
from .role.role_registry import RoleRegistry
from .service_collection import ServiceColletion
from .service_collection_filter.service_collection_filter import ServiceCollectionFilter
from .service_provider.service_provider import ServiceProvider


def get_custom_constructor_parameters(wrapped_class: Type):
    constructor_parameters = inspect.signature(
        wrapped_class.__init__
    ).parameters.items()

    for name, type_name in constructor_parameters:
        match str(type_name):
            case "**kwargs":
                continue
            case "*args":
                continue
            case "self":
                continue

        yield (name, type_name)


def get_injectable_constructor_parameters(
    wrapped_class: Type,
) -> Generator[
    Tuple[str, Type, Sequence[ServiceCollectionFilter]],
    None,
    None,
]:
    for name, type_name in get_custom_constructor_parameters(wrapped_class):
        if inspect.isclass(type_name.annotation):
            if type_name.annotation is inspect._empty:
                raise Exception(
                    f"all of the service arguments need to be typed in {wrapped_class} {type_name}"
                )
            else:
                yield (name, type_name.annotation, ())
        else:
            if isinstance(type_name.annotation, Role):
                yield (name, get_root_class(type_name.annotation), ())
            elif get_origin(type_name.annotation) is Annotated:
                annotation_args = get_args(type_name.annotation)

                yield (name, annotation_args[0], annotation_args[1:])
            else:
                raise Exception(f"uninjectable type {type_name.annotation}")


class DependencyInjectionContainer:
    def __init__(
        self,
        role_registry: RoleRegistry,
    ):
        self.instantiated_services: dict[Type, object] = {}
        self.service_providers_roles: dict[Type, Tuple[Role, Type]] = {}
        self.role_registry = role_registry

    def make(self, cls):
        if cls in self.instantiated_services:
            return self.instantiated_services[cls]

        root_cls = get_root_class(cls)

        if root_cls not in self.service_providers_roles:
            raise Exception(
                f"{cls} is not a service and there is no service provider registered for it"
            )

        _, provider_cls = self.service_providers_roles[root_cls]

        args = {}

        for (
            name,
            type_class,
            service_collection_filters,
        ) in get_injectable_constructor_parameters(provider_cls):
            if issubclass(type_class, ServiceColletion):
                args[name] = self.make_service_collection(service_collection_filters)
            else:
                args[name] = self.make(type_class)

        instantiated_provider = provider_cls(**args)
        instantiated_service = None

        if isinstance(instantiated_provider, ServiceProvider):
            instantiated_service = instantiated_provider.provide()
        else:
            instantiated_service = instantiated_provider

        self.register_instance(cls, instantiated_service)

        return instantiated_service

    def make_service_collection(
        self,
        service_collection_filters: Sequence[ServiceCollectionFilter],
    ):
        services = set()

        for service_collection_filter in service_collection_filters:
            for provided_class, (
                role,
                wrapped_class,
            ) in self.service_providers_roles.items():
                if service_collection_filter.should_include(role, provided_class):
                    services.add((role, self.make(provided_class)))

        return ServiceColletion(services)

    def prepare(self):
        for role, wrapped_class in self.role_registry.filter_by_role_class(service):
            provided_class = None

            if isinstance(role, service_provider_wrapped):
                provided_class = role.provides
            else:
                provided_class = wrapped_class

            if provided_class in self.service_providers_roles:
                raise Exception(
                    f"service provider for {provided_class} is already registered"
                )

            self.service_providers_roles[provided_class] = (role, wrapped_class)

    def register_instance(self, cls, instance):
        self.instantiated_services[cls] = instance
