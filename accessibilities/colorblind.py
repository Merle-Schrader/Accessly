from accessly import register_feature, config
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb, to_hex, to_rgba
import numpy as np

def apply(cb_options):
    """
    Registers a colorblind accessibility hook that recolors problematic
    plot elements before rendering.

    Args:
        cb_options (dict): {
            "types": str or list of str  (e.g., "redgreen")
        }
    """
    if not isinstance(cb_options, dict):
        print("[Colorblind] WARNING: Expected dict, got", type(cb_options))
        return

    cb_types = cb_options.get("types", [])
    if isinstance(cb_types, str):
        cb_types = [cb_types]

    def recolor_current_figure():
        fig = plt.gcf()
        for ax in fig.axes:
            # Lines
            for line in ax.get_lines():
                _try_recolor(line.set_color, line.get_color(), cb_types)

            # Scatter
            for col in ax.collections:
                try:
                    facecolors = col.get_facecolors()
                    if facecolors is not None and len(facecolors) > 0:
                        new_colors = []
                        for rgba in facecolors:
                            rgb = rgba[:3]
                            new_rgb = remap_rgb_to_safe(rgb, cb_types)
                            new_colors.append(to_rgba(new_rgb, alpha=rgba[3]))
                        col.set_facecolors(new_colors)

                    edgecolors = col.get_edgecolors()
                    if edgecolors is not None and len(edgecolors) > 0:
                        new_edges = []
                        for rgba in edgecolors:
                            rgb = rgba[:3]
                            new_rgb = remap_rgb_to_safe(rgb, cb_types)
                            new_edges.append(to_rgba(new_rgb, alpha=rgba[3]))
                        col.set_edgecolors(new_edges)

                except Exception as e:
                    print(f"[Colorblind] Scatter recolor failed: {e}")

            # Bars/histograms
            for patch in ax.patches:
                _try_recolor(patch.set_facecolor, patch.get_facecolor(), cb_types)

            # Filled areas
            for poly in ax.collections:
                if hasattr(poly, "get_facecolors"):
                    try:
                        fc = poly.get_facecolors()
                        if fc is not None and len(fc) > 0:
                            new_colors = []
                            for rgba in fc:
                                rgb = rgba[:3]
                                new_rgb = remap_rgb_to_safe(rgb, cb_types)
                                new_colors.append(to_rgba(new_rgb, alpha=rgba[3]))
                            poly.set_facecolors(new_colors)
                    except Exception as e:
                        print(f"[Colorblind] fill_between recolor failed: {e}")

            # Error bars
            if hasattr(ax, "containers"):
                for container in ax.containers:
                    for artist in container:
                        if hasattr(artist, "get_facecolor"):
                            _try_recolor(artist.set_facecolor, artist.get_facecolor(), cb_types)

            # Legend
            legend = ax.get_legend()
            if legend:
                try:
                    handles, _ = ax.get_legend_handles_labels()
                    for handle in handles:
                        if hasattr(handle, "get_color"):
                            _try_recolor(handle.set_color, handle.get_color(), cb_types)
                        elif hasattr(handle, "get_facecolor"):
                            _try_recolor(handle.set_facecolor, handle.get_facecolor(), cb_types)

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


def _try_recolor(setter_func, original_color, cb_types):
    try:
        rgb = to_rgb(original_color)
        new_rgb = remap_rgb_to_safe(rgb, cb_types)
        hex_new = to_hex(new_rgb)
        # if hex_new != to_hex(rgb):
        #     print(f"[Colorblind] Adjusted {to_hex(rgb)} → {hex_new}")
        setter_func(hex_new)
    except Exception as e:
        print(f"[Colorblind] Failed to recolor: {e}")


def remap_rgb_to_safe(rgb, cb_types):
    rgb_vec = np.array(rgb)
    for cb in cb_types:
        basis = SAFE_RGB_BASES.get(cb)
        if basis is not None:
            # Recombine R, G, B with new anchor vectors
            new_rgb = (
                rgb_vec[0] * basis[:, 0] +
                rgb_vec[1] * basis[:, 1] +
                rgb_vec[2] * basis[:, 2]
            )
            return np.clip(new_rgb, 0, 1)
    return rgb_vec



# Define safe color basis (rows = R, G, B projections)
# For red-green colorblindness, map:
# - Red → Sand (#F4A460)
# - Green → Blue (#4682B4)
# - Blue → Gray (#A9A9A9)

SAFE_RGB_BASES = {
    "redgreen": np.array([
        [244,  70, 169],  # R
        [164, 130, 169],  # G
        [ 96, 180, 169],  # B
    ], dtype=float).T / 255.0,
    "protanopia": np.array([
        [244,  70, 169],
        [164, 130, 169],
        [ 96, 180, 169],
    ]) / 255.0,
    "deuteranopia": np.array([
        [244,  70, 169],
        [164, 130, 169],
        [ 96, 180, 169],
    ]) / 255.0
}

# Register the colorblind feature with Accessly
register_feature("colorblind", apply)
