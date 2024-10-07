import os
import dearpygui.dearpygui as dpg
import stages

os.system("cls")
dpg.create_context()

TOPICS = [
    "FLSM",
    "  IP -> Propiedades",
    "  IP -> Host",
    "  Host -> IP",
    "  Host -> Subred",
    "  Subred -> IP & Broadcast",
    "VLSM",
]
MODBUS = [
    "RTU",
    "ASCII",
    "TCP",
]


ROOT = os.path.dirname(os.path.abspath(__file__))


def absolute_path(relative_path):
    return os.path.join(ROOT, relative_path)


# ==============================================================================
# CALLBACKS
# ==============================================================================
def select_topic(sender, app_data, user_data):
    for i in range(len(TOPICS + MODBUS)):
        if sender != f"topic_{i}":
            dpg.set_value(f"topic_{i}", False)

    dpg.delete_item("usage", children_only=True)
    stage = getattr(stages, sender, stages.topic_nan)
    stage()


# ==============================================================================
# FONT REGISTRY
# ==============================================================================

with dpg.font_registry():
    dpg.add_font(absolute_path("ttf/FiraCode-Medium.ttf"), 18, tag="default")
    dpg.add_font(absolute_path("ttf/FiraCode-Bold.ttf"), 18, tag="bold_s")
    dpg.add_font(absolute_path("ttf/FiraCode-Bold.ttf"), 20, tag="bold")

dpg.bind_font("default")

# ==============================================================================
# VALUES REGISTRY
# ==============================================================================
with dpg.value_registry():
    dpg.add_int4_value(tag="ip", default_value=[0, 0, 0, 0])
    dpg.add_int_value(tag="v1", default_value=0)
    dpg.add_int_value(tag="v2", default_value=0)
    dpg.add_string_value(tag="v3", default_value="")

# ==============================================================================
# HANDLER REGISTRY
# ==============================================================================


# ==============================================================================
# MAIN WINDOW
# ==============================================================================
with dpg.window(tag="main"):
    with dpg.group(horizontal=True):
        with dpg.child_window(width=250):
            dpg.add_text("Subnetting")
            dpg.bind_item_font(dpg.last_item(), "bold_s")
            for i, label in enumerate(TOPICS):
                dpg.add_selectable(
                    label=label,
                    tag=f"topic_{i}",
                    callback=select_topic,
                )
            dpg.add_separator()
            dpg.add_text("Modbus")
            dpg.bind_item_font(dpg.last_item(), "bold_s")
            for i, label in enumerate(MODBUS, start=len(TOPICS)):
                dpg.add_selectable(
                    label=label,
                    tag=f"topic_{i}",
                    callback=select_topic,
                )

        with dpg.child_window(tag="usage"):
            dpg.add_text("Redes Industriales", tag="title")
            dpg.add_text("Seleccione un tema para comenzar")
            dpg.add_spacer()
            dpg.add_text("Desarrollado por:")
            dpg.add_text("  - Cesar Adolfo, Cruz Vargaya")

dpg.bind_item_font("title", "bold")

# ==============================================================================
# THEMES
# ==============================================================================


# ==============================================================================
# RUN
# ==============================================================================
dpg.create_viewport(
    title="Redes Industriales",
    width=1500,
    height=800,
    always_on_top=True,
)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("main", True)
dpg.start_dearpygui()
dpg.destroy_context()
