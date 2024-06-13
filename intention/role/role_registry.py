from typing import Type


class RoleRegistry:
    def __init__(self):
        self.registry = set()

    def filter_by_role_class(self, role_class):
        for role, wrapped_class in self.registry:
            if isinstance(role, role_class):
                yield (role, wrapped_class)

    def register(self, role, wrapped_class: Type):
        self.registry.add((role, wrapped_class))
