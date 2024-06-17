from typing import TYPE_CHECKING, Any

from .role_registry import RoleRegistry

# Only import for type checking to avoid circular import issues
if TYPE_CHECKING:
    from .role import Role

    role_registry_global: RoleRegistry[Role] = RoleRegistry()
else:
    role_registry_global: RoleRegistry[Any] = RoleRegistry()
