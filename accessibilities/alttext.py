from accessly import register_feature
from accessly import config
import matplotlib.pyplot as plt

def apply(params):
    """
    Adds 'L' and 'R' labels to plots for distinguishing between the left and right side of the plot.
    Parameters:
        position (str): 'top' or 'bottom'
        alpha (float): label transparency (default: 1.0)
        color (str): label color (default: black)
        fontsize (int): font size (default: 14)
    """
    position = params if isinstance(params, str) else params.get("position", "bottom")
    description = params.get("description", "Please add alt-text using the description keyword.")
    alpha = params.get("alpha", 1.0)
    color = params.get("color", "black")
    fontsize = params.get("fontsize", 14)

    def add_alttext():
        fig = plt.gcf()
        for ax in fig.axes:

            y_pos = 1.05 if position == "top" else -0.1
            va = "bottom" if position == "top" else "top"

            ax.text(0.01, y_pos, "Alt text: " + str(description),
                    fontsize=fontsize, fontname="Arial",
                    color=color, alpha=alpha, ha="left", va=va,
                    transform=ax.transAxes, clip_on=False)
            print("\nAlt text: " + str(description))



    config.show_hooks.append(add_alttext)


register_feature("alttext", apply)
