import importlib, pkgutil
from core.skill_base import Skill

def load_skills(package="skills"):
    registry = {}
    pkg = importlib.import_module(package)
    for _, mod_name, _ in pkgutil.iter_modules(pkg.__path__):
        mod = importlib.import_module(f"{package}.{mod_name}")
        for obj in vars(mod).values():
            if (isinstance(obj, type) and issubclass(obj, Skill)
                    and obj is not Skill):
                registry[obj.name] = obj()
    return registry
