import importlib
import pkgutil
from types import ModuleType


def import_all_from(
    module: ModuleType,
    is_recursive: bool = True,
) -> None:
    for loader, name, is_pkg in pkgutil.walk_packages(module.__path__):
        if name.startswith("test_"):
            continue

        full_name = module.__name__ + "." + name

        try:
            imported = importlib.import_module(full_name)

            if is_recursive and is_pkg:
                import_all_from(imported, is_recursive)
        except ModuleNotFoundError:
            continue
