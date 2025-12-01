from aom_menu import register_menus
from utils import _log, _err


def _startup():
    try:
        register_menus()
        _log("[AutoOverViewMeshes] Menus registered")
    except Exception as e:
        _err(f"[AutoOverViewMeshes] Menu registration failed: {e}")


_startup()
