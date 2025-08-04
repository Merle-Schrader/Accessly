import matplotlib.pyplot as plt
from . import config
from .accessibilities import load_all_accessibility_features

_original_show = plt.show
_loaded_accessibilities = False

def configure(**kwargs):
    """
    Called by the user to enable accessibility features.

    Example:
        configure(colorblind="deuteranopia")
    """
    global _loaded_accessibilities

    if not _loaded_accessibilities:
        load_all_accessibility_features()  # auto-import modules
        _loaded_accessibilities = True

    config.settings.update(kwargs)

    for name, handler in config.registered_features.items():
        if name in kwargs and kwargs[name]:
            handler(kwargs[name])  # call apply function

    _monkey_patch_matplotlib()


def register_feature(name, handler_func):
    """
    Used by feature modules to register themselves.
    Example: register_feature("colorblind", apply)
    """
    config.registered_features[name] = handler_func


def _monkey_patch_matplotlib():
    """
    Monkey-patches matplotlib's show() to trigger modifications.
    """
    def patched_show(*args, **kwargs):
        _original_show(*args, **kwargs)

    plt.show = patched_show
