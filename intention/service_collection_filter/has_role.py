from typing import Any, Type
from ..role.role import Role
from .service_collection_filter import ServiceCollectionFilter


class HasRole(ServiceCollectionFilter):
    def __init__(self, role: Type[Role]):
        self.role = role

    def should_include(self, role: Role, provided_class: Type[Any]) -> bool:
        return isinstance(role, self.role)
