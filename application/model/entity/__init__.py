import pkgutil
from pathlib import Path


def load_all_models() -> list[str]:
    """Load all models from this folder."""
    package_dir = Path(__file__).resolve().parent
    modules = pkgutil.walk_packages(
        path=[str(package_dir)],
        prefix="application.model.entity.",
    )

    list = []
    for module in modules:
        list.append(module.name)

    return list
