from Accessly import register_feature
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb, to_hex
import colorsys

def apply(cb_type):
    def recolor_figure(event):
        fig = event.canvas.figure
        for ax in fig.axes:
            for line in ax.get_lines():
                color = line.get_color()
                try:
                    rgb = to_rgb(color)
                    if is_problematic(rgb, cb_type):
                        new_color = shift_color(rgb, cb_type)
                        line.set_color(new_color)
                except Exception:
                    pass  # non-standard color or error

    plt.gcf().canvas.mpl_connect("draw_event", recolor_figure)


def is_problematic(rgb, cb_type):
    r, g, b = rgb
    if cb_type == "protanopia":       # red-weak
        return r > g and r > b
    elif cb_type == "deuteranopia":   # green-weak
        return g > r and g > b
    elif cb_type == "tritanopia":     # blue-weak
        return b > r and b > g
    return False


def shift_color(rgb, cb_type):
    r, g, b = rgb
    h, l, s = colorsys.rgb_to_hls(r, g, b)

    # shift hue from problematic region
    if cb_type == "protanopia":
        h = (h + 0.1) % 1.0  # move red to yellow
    elif cb_type == "deuteranopia":
        h = (h - 0.1) % 1.0  # move green to blue
    elif cb_type == "tritanopia":
        h = (h + 0.15) % 1.0  # move blue to green

    r_new, g_new, b_new = colorsys.hls_to_rgb(h, l, s)
    return to_hex((r_new, g_new, b_new))


register_feature("colorblind", apply)
