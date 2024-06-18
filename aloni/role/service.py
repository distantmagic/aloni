from .role import Role
from .service_override_behavior import ServiceOverrideBehavior


class service(Role):
    override_behavior: ServiceOverrideBehavior = ServiceOverrideBehavior.DENY
