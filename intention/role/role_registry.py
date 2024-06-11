from typing import Type


class RoleRegistry:
    def __init__(self):
        self.registry = set()

    def register(self, role, wrapped_class: Type):
        self.registry.add((role, wrapped_class))
