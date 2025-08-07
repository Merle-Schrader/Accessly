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

    line_type = string(line_options.get("types", []))
    #if isinstance(line_types, str):
    #    line_types = [line_types]

    def restyle_current_figure():
        fig = plt.gcf()
        for ax in fig.axes:
            # Lines
            lines = ax.get_lines()
            if len(lines) == 0:
                raise Exception("[Linestyles] No lines found")
            elif len(lines) > 14:
                raise Exception("[Linestyles] Too many lines found, unable to make accessible")
            elif len(lines) <= 4:
                styles = ['solid', 'dotted', 'dashed', 'dashdot']
            else:
                styles = [ 
                    'solid',
                    (0, (1, 10)),
                    (0, (1, 5)),
                    (0, (1, 1)),
                    (5, (10, 3)),
                    (0, (5, 10)),
                    (0, (5, 5)),
                    (0, (5, 1)),
                    (0, (3, 10, 1, 10)),
                    (0, (3, 5, 1, 5)),
                    (0, (3, 1, 1, 1)),
                    (0, (3, 5, 1, 5, 1, 5)),
                    (0, (3, 10, 1, 10, 1, 10)),
                    (0, (3, 1, 1, 1, 1, 1)),
                    ]

            for line in lines:
                if 'bold' in line_type:
                    line.set_linewidth( 3 )
                if 'diff' in line_type:
                    idx = lines.index(line)
                    line.set_style( styles[idx] )
                #if 'recolor' in line_type:

            '''
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
            '''

    config.show_hooks.append(restyle_current_figure)


# Register the colorblind feature with Accessly
register_feature("linestyles", apply)
