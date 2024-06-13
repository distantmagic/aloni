import importlib
import pkgutil


def import_all_from(module, is_recursive=True):
    for loader, name, is_pkg in pkgutil.walk_packages(module.__path__):
        full_name = module.__name__ + "." + name

        try:
            imported = importlib.import_module(full_name)

            if is_recursive and is_pkg:
                import_all_from(imported, is_recursive)
        except ModuleNotFoundError:
            continue
