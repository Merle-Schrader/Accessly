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
            print(f"Calling handler for {name} with value: {kwargs[name]}")

    _monkey_patch_matplotlib()


def register_feature(name, handler_func):
    """
    Used by feature modules to register themselves.
    Example: register_feature("colorblind", apply)
    """
    config.registered_features[name] = handler_func


def _monkey_patch_matplotlib():
    def patched_show(*args, **kwargs):
        # Call all registered show hooks before actually showing
        for hook in config.show_hooks:
            try:
                hook()
            except Exception as e:
                print(f"[accessly] Warning: show hook failed: {e}")
        _original_show(*args, **kwargs)

    plt.show = patched_show

