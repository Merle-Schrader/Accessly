from accessly import register_feature, config
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from pyfonts import load_google_font

def apply(lf_options):
    """
    Registers a font style accessibility hook that changes all plot
    text options to a selected font, that may be useful for dyslexic
    or low-vision users.

    Args:
        lf_options (dict): {
            "font": str  (e.g., "Comic Sans MS")
        }
    """
    if not isinstance(lf_options, dict):
        print("[LegibleFont] WARNING: Expected dict, got", type(lf_options))
        return

    lf_font = lf_options.get("font", [])
    if isinstance(lf_font, str):
        lf_font = [lf_font]
        # TO DO - make it so only one string accepted

    def font_update_current_figure():
        fig = plt.gcf()


        print(plt.rcParams["font.sans-serif"][0])
        print(plt.rcParams["font.monospace"][0])
        plt.rcParams["font.family"] = "sans-serif"
        plt.rcParams["font.sans-serif"] = ["Arial"]




        # for ax in fig.axes:

        #     for x in ax.get_xlabel():
        #         x
        #         try:
        #             x.get_font

                    
                # except Exception as e:
                #     print(f"[LegibleFont] Label Font Change Failed: {e}")

            # label, title,legend handle labels, x and y
            # # Scatter
            # for col in ax.collections:
            #     try:
            #         facecolors = col.get_facecolors()
            #         if facecolors is not None and len(facecolors) > 0:
            #             new_colors = []
            #             for rgba in facecolors:
            #                 rgb = rgba[:3]
            #                 new_rgb = remap_rgb_to_safe(rgb, cb_types)
            #                 new_colors.append(to_rgba(new_rgb, alpha=rgba[3]))
            #             col.set_facecolors(new_colors)

            #         edgecolors = col.get_edgecolors()
            #         if edgecolors is not None and len(edgecolors) > 0:
            #             new_edges = []
            #             for rgba in edgecolors:
            #                 rgb = rgba[:3]
            #                 new_rgb = remap_rgb_to_safe(rgb, cb_types)
            #                 new_edges.append(to_rgba(new_rgb, alpha=rgba[3]))
            #             col.set_edgecolors(new_edges)

            #     except Exception as e:
            #         print(f"[Colorblind] Scatter recolor failed: {e}")


    config.show_hooks.append(font_update_current_figure)


# Register the feature with Accessly
register_feature("legiblefont", apply)