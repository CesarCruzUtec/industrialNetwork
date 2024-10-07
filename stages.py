import dearpygui.dearpygui as dpg
import functions as f


def stage_func(func):
    def wrapper(*args, **kwargs):
        dpg.push_container_stack("usage")
        with dpg.stage(tag="stage_0"):
            func(*args, **kwargs)
            with dpg.child_window(tag="solution", border=False):
                pass
        dpg.unstage("stage_0")
        dpg.delete_item("stage_0")
        dpg.pop_container_stack()

    return wrapper


# ==============================================================================
# CALLBACKS
# ==============================================================================
def test(sender, app_data, user_data):
    print(sender, app_data, user_data)


# ==============================================================================
# STAGE
# ==============================================================================
@stage_func
def topic_nan():
    dpg.add_text("Not implemented yet")


def add_ip_input():
    dpg.add_input_intx(
        label="IP",
        min_value=0,
        min_clamped=True,
        max_value=255,
        max_clamped=True,
        size=4,
        source="ip",
        width=300,
    )


def add_extra_value(label, src):
    dpg.add_input_int(
        label=label,
        min_value=1,
        min_clamped=True,
        source=src,
        width=300,
        default_value=1,
    )


@stage_func  # FLSM
def topic_0():
    add_ip_input()
    add_extra_value("# de subredes", "v1")
    dpg.add_button(label="Calcular", callback=f.topic_0)
    dpg.add_separator()


@stage_func  # IP -> Propiedades
def topic_1():
    add_ip_input()
    add_extra_value("Máscara", "v1")
    dpg.add_button(label="Calcular", callback=f.topic_1)
    dpg.add_separator()


@stage_func  # IP -> Host
def topic_2():
    add_ip_input()
    add_extra_value("Máscara", "v1")
    dpg.add_button(label="Calcular", callback=f.topic_2)
    dpg.add_separator()


@stage_func  # Host -> IP
def topic_3():
    add_ip_input()
    add_extra_value("Máscara", "v1")
    add_extra_value("# de host", "v2")
    dpg.add_button(label="Calcular", callback=f.topic_3)
    dpg.add_separator()


@stage_func  # Host -> Subred
def topic_4():
    add_ip_input()
    add_extra_value("Máscara", "v1")
    dpg.add_button(label="Calcular", callback=f.topic_4)
    dpg.add_separator()


@stage_func  # Subred -> IP & Broadcast
def topic_5():
    add_extra_value("Subred", "v1")
    add_ip_input()
    add_extra_value("Máscara", "v2")
    dpg.add_button(label="Calcular", callback=f.topic_5)
    dpg.add_separator()


@stage_func  # VLSM
def topic_6():
    add_ip_input()
    add_extra_value("Máscara", "v1")
    dpg.add_input_text(
        label="Número de hosts",
        source="v3",
        hint="Separados por guiones",
        decimal=True,
        no_spaces=True,
        width=300,
    )
    dpg.add_button(label="Calcular", callback=f.topic_6)
    dpg.add_separator()
