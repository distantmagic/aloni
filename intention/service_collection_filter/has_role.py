from typing import Any, Type
from ..role.role import Role
from .service_collection_filter import ServiceCollectionFilter


class HasRole(ServiceCollectionFilter):
    def __init__(self, role: Type[Role[Any]]):
        self.role = role

    def should_include(self, role: Role[Any], provided_class: Type[Any]) -> bool:
        return isinstance(role, self.role)
