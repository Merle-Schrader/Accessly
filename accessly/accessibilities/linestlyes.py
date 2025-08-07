from accessly import register_feature, config
import matplotlib.pyplot as plt
import numpy as np

def apply(line_options):
    """
    Registers a linestlye accessibility hook that restyles problematic
    plot elements before rendering.

    Args:
        line_options (dict): {
            "types": str or list of str
            Options:
                     'bold': changes all to solid-bold without recoloring
                     'bold-recolor': changes all to solid-bold and also recolors
                     'diff': changes all to different styles wihtout recoloring
                     'diff-recolor': changes all to different styles and also recolors
        }
    """
    if not isinstance(line_options, dict):
        print("[Linestyles] WARNING: Expected dict, got", type(line_options))
        return

    line_types = line_options.get("types", [])
    if isinstance(line_types, str):
        line_types = [line_types]

    def restyle_current_figure():
        fig = plt.gcf()
        for ax in fig.axes:
            # Lines
            for line in ax.get_lines():
                _try_recolor(line.set_color, line.get_color(), line_types)


            # Legend
            legend = ax.get_legend()
            if legend:
                try:
                    handles, _ = ax.get_legend_handles_labels()
                    for handle in handles:
                        if hasattr(handle, "get_color"):
                            _try_recolor(handle.set_color, handle.get_color(), line_types)
                        elif hasattr(handle, "get_facecolor"):
                            _try_recolor(handle.set_facecolor, handle.get_facecolor(), line_types)

                    props = {
                        "loc": getattr(legend, "_loc", "best"),
                        "frameon": legend.get_frame_on(),
                        "title": legend.get_title().get_text(),
                        "ncol": getattr(legend, "_ncol", 1),
                        "fontsize": legend.prop.get_size() if hasattr(legend, "prop") else None,
                    }

                    legend.remove()
                    ax.legend(handles=handles, **{k: v for k, v in props.items() if v is not None})

                except Exception as e:
                    print(f"[Colorblind] Legend recolor failed: {e}")

    config.show_hooks.append(recolor_current_figure)


def _try_restyle(setter_func, original_style, line_types):
    try:
        rgb = to_rgb(original_style)
        new_rgb = remap_rgb_to_safe(rgb, line_types)
        # if hex_new != to_hex(rgb):
        #     print(f"[Linestyle] Adjusted {} → {hex_new}")
        setter_func(hex_new)
    except Exception as e:
        print(f"[Linetyles] Failed to restyle: {e}")


def remap_rgb_to_safe(rgb, line_types):
    rgb_vec = np.array(rgb)
    for line in line_types:
        basis = SAFE_RGB_BASES.get(line)
        if basis is not None:
            # Recombine R, G, B with new anchor vectors
            new_rgb = (
                rgb_vec[0] * basis[:, 0] +
                rgb_vec[1] * basis[:, 1] +
                rgb_vec[2] * basis[:, 2]
            )
            return np.clip(new_rgb, 0, 1)
    return rgb_vec




# Register the colorblind feature with Accessly
register_feature("linestyles", apply)
