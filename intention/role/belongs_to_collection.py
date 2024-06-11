from .role import Role


class belongs_to_collection(Role):
    def __init__(self, name: str):
        pass

    def __call__(self, cls):
        return cls
