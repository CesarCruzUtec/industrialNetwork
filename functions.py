import dearpygui.dearpygui as dpg
import math


def back_func(func):
    def wrapper(s, a, u):
        dpg.delete_item("solution", children_only=True)
        dpg.push_container_stack("solution")
        with dpg.stage(tag="stage_1"):
            try:
                func(s, a, u)
            except Exception as e:
                dpg.add_text(str(e), color=(255, 0, 0), wrap=0)
        dpg.unstage("stage_1")
        dpg.delete_item("stage_1")
        dpg.pop_container_stack()

    return wrapper


def add_ip(ip, n):
    # IP = [xxx, xxx, xxx, xxx]
    # Add n to the IP address

    ip_long = sum([ip[i] * 256 ** (3 - i) for i in range(4)])
    ip_long += n
    ip = [ip_long // 256 ** (3 - i) % 256 for i in range(4)]

    return ip


@back_func
def topic_0(sender, app_data, user_data):
    # Paso 0: Obtener los datos
    ip = dpg.get_value("ip")
    n = dpg.get_value("v1")

    # Paso 1: Identificar la clase
    dpg.add_text("Paso 1: Identificar la clase", tag="p1")

    if ip[0] < 128:
        clase = 8
        clase_ = "A"
        mask = [255, 0, 0, 0]
    elif ip[0] < 192:
        clase = 16
        clase_ = "B"
        mask = [255, 255, 0, 0]
    elif ip[0] < 224:
        clase = 24
        clase_ = "C"
        mask = [255, 255, 255, 0]
    else:
        dpg.add_text(
            "No se puede realizar FLSM en direcciones de clase D o E",
            color=(255, 0, 0),
        )
        return

    ip_str = ".".join(map(str, ip))
    dpg.add_text(f"La dirección IP {ip_str} pertenece a la clase {clase_}")
    mask_str = ".".join(map(str, mask))
    dpg.add_text(f"La máscara de red es {mask_str} / {clase}")
    mask_bin = ".".join(map(lambda x: bin(x)[2:].zfill(8), mask))
    dpg.add_text(f"Máscara de red en binario: {mask_bin}")
    dpg.add_separator()

    # Paso 2: Obtener N
    dpg.add_text("Paso 2: Obtener N", tag="p2")

    N = math.ceil(math.log2(n))
    dpg.add_text(f"Bits de subred: {N}")
    dpg.add_text(f"Hay {2**N-n} subredes en desuso")
    dpg.add_separator()

    # Paso 3: Obtener la nueva máscara
    dpg.add_text("Paso 3: Obtener la nueva máscara", tag="p3")

    mask_new = mask.copy()
    mask_new[clase // 8] = 256 - 2 ** (8 - N)
    mask_new_str = ".".join(map(str, mask_new))
    dpg.add_text(f"La nueva máscara de red es {mask_new_str} / {clase+N}")
    mask_new_bin = ".".join(map(lambda x: bin(x)[2:].zfill(8), mask_new))
    dpg.add_text(f"Máscara de red en binario: {mask_new_bin}")
    dpg.add_separator()

    # Paso 4: Obtener número de host por subred
    dpg.add_text("Paso 4: Obtener número de host por subred", tag="p4")

    M = 32 - clase - N
    dpg.add_text(f"Bits de host: {M}")
    H = 2**M - 2
    dpg.add_text(f"Número de host por subred: {H}")
    dpg.add_separator()

    # Paso 5: Obtener el salto de red
    dpg.add_text("Paso 5: Obtener el salto de red", tag="p5")

    X = 256 - mask_new[clase // 8]
    dpg.add_text(f"Salto de red: {X}")
    dpg.add_separator()

    # Paso 6: Obtener la tabla de subredes
    dpg.add_text("Paso 6: Obtener la tabla de subredes", tag="p6")

    X = X * 256 ** (3 - clase // 8)
    with dpg.table(
        header_row=True,
        delay_search=True,
        borders_outerH=True,
        borders_outerV=True,
        borders_innerV=True,
        no_host_extendX=True,
        row_background=True,
        policy=dpg.mvTable_SizingFixedFit,
        tag="table",
    ):
        dpg.add_table_column(label="N°")
        dpg.add_table_column(label="IP Subred")
        dpg.add_table_column(label="Primer Host")
        dpg.add_table_column(label="Último Host")
        dpg.add_table_column(label="Broadcast")

        for i in range(n):
            ip_str = ".".join(map(str, add_ip(ip.copy(), i * X)))
            first_host = ".".join(map(str, add_ip(ip.copy(), i * X + 1)))
            last_host = ".".join(map(str, add_ip(ip.copy(), (i + 1) * X - 2)))
            broadcast = ".".join(map(str, add_ip(ip.copy(), (i + 1) * X - 1)))

            with dpg.table_row():
                dpg.add_text(str(i + 1))
                dpg.add_text(ip_str)
                dpg.add_text(first_host)
                dpg.add_text(last_host)
                dpg.add_text(broadcast)

    for i in range(1, 7):
        dpg.bind_item_font(f"p{i}", "bold")
        dpg.configure_item(f"p{i}", color=(0, 255, 0))


@back_func
def topic_1(sender, app_data, user_data):
    # Paso 0: Obtener los datos
    ip = dpg.get_value("ip")
    clase = dpg.get_value("v1")
    if clase == 0:
        clase = sum([8 if ip[0] < i else 0 for i in [128, 192, 224]])
        dpg.set_value("v1", clase)

    # Paso 1: Pasar a binario la IP de red
    dpg.add_text("Paso 1: Pasar a binario la IP de red", tag="p1")

    clase_base = 8 * (clase // 8)
    N = clase - clase_base
    mask = [255 if i * 8 < clase_base else 0 for i in range(4)]
    mask[clase // 8] = 256 - 2 ** (8 - N)
    mask_str = ".".join(map(str, mask))
    dpg.add_text(f"La máscara de red es {mask_str} / {clase}")
    mask_bin = ".".join(map(lambda x: bin(x)[2:].zfill(8), mask))
    dpg.add_text(f"Máscara de red en binario: {mask_bin}")
    dpg.add_separator()

    # Paso 2: Pasar a binario el IP host
    dpg.add_text("Paso 2: Pasar a binario el IP host", tag="p2")

    ip_bin = ".".join(map(lambda x: bin(x)[2:].zfill(8), ip))
    dpg.add_text(f"La dirección IP en binario es {ip_bin}")
    dpg.add_separator()

    # Paso 3: Usar AND para obtener la IP de subred
    dpg.add_text("Paso 3: Usar AND para obtener la IP de subred", tag="p3")

    ip_subred = [ip[i] & mask[i] for i in range(4)]
    ip_subred_str = ".".join(map(str, ip_subred))
    dpg.add_text(f"La dirección IP de subred es {ip_subred_str}")
    ip_subred_bin = ".".join(map(lambda x: bin(x)[2:].zfill(8), ip_subred))
    dpg.add_text(f"La dirección IP de subred en binario es {ip_subred_bin}")
    dpg.add_separator()

    # Paso 4: Usar OR para obtener la IP de broadcast
    dpg.add_text("Paso 4: Usar OR para obtener la IP de broadcast", tag="p4")

    mask_inv = [255 - i for i in mask]
    ip_broadcast = [ip[i] | mask_inv[i] for i in range(4)]
    ip_broadcast_str = ".".join(map(str, ip_broadcast))
    dpg.add_text(f"La dirección IP de broadcast es {ip_broadcast_str}")
    ip_broadcast_bin = ".".join(map(lambda x: bin(x)[2:].zfill(8), ip_broadcast))
    dpg.add_text(f"La dirección IP de broadcast en binario es {ip_broadcast_bin}")
    dpg.add_separator()

    # Paso 5: Mostar la tabla
    dpg.add_text("Paso 5: Tabla de direcciones", tag="p5")

    with dpg.table(
        header_row=True,
        delay_search=True,
        borders_outerH=True,
        borders_outerV=True,
        borders_innerV=True,
        no_host_extendX=True,
        row_background=True,
        policy=dpg.mvTable_SizingFixedFit,
        tag="table",
    ):
        dpg.add_table_column(label="IP Subred")
        dpg.add_table_column(label="Primer Host")
        dpg.add_table_column(label="Último Host")
        dpg.add_table_column(label="Broadcast")

        with dpg.table_row():
            dpg.add_text(ip_subred_str)
            dpg.add_text(".".join(map(str, add_ip(ip_subred.copy(), 1))))
            dpg.add_text(".".join(map(str, add_ip(ip_broadcast.copy(), -1))))
            dpg.add_text(ip_broadcast_str)

    for i in range(1, 6):
        dpg.bind_item_font(f"p{i}", "bold")
        dpg.configure_item(f"p{i}", color=(0, 255, 0))


@back_func
def topic_2(sender, app_data, user_data):
    # Paso 0: Obtener los datos
    ip = dpg.get_value("ip")
    clase = dpg.get_value("v1")
    if clase == 0:
        clase = sum([8 if ip[0] < i else 0 for i in [128, 192, 224]])
        dpg.set_value("v1", clase)

    # Paso 1: Pasar a binario la IP de host
    dpg.add_text("Paso 1: Pasar a binario la IP de host", tag="p1")

    ip_bin = ".".join(map(lambda x: bin(x)[2:].zfill(8), ip))
    dpg.add_text(f"La dirección IP en binario es {ip_bin}")
    dpg.add_separator()

    # Paso 2: Pasar a binario la máscara de red
    dpg.add_text("Paso 2: Pasar a binario la máscara de red", tag="p2")

    clase_base = 8 * (clase // 8)
    N = clase - clase_base
    mask = [255 if i * 8 < clase_base else 0 for i in range(4)]
    mask[clase // 8] = 256 - 2 ** (8 - N)
    mask_str = ".".join(map(str, mask))
    dpg.add_text(f"La máscara de red es {mask_str} / {clase}")
    mask_bin = ".".join(map(lambda x: bin(x)[2:].zfill(8), mask))
    dpg.add_text(f"Máscara de red en binario: {mask_bin}")
    dpg.add_separator()

    # Paso 3: Usar AND para obtener el número de host
    dpg.add_text("Paso 3: Usar AND para obtener el número de host", tag="p3")

    mask_inv = [255 - i for i in mask]
    H_ip = [ip[i] & mask_inv[i] for i in range(4)]
    H_ip_str = ".".join(map(str, H_ip))
    dpg.add_text(f"La dirección IP de host es {H_ip_str}")
    H = sum([H_ip[i] * 256 ** (3 - i) for i in range(4)])
    dpg.add_text(f"El número de host es {H}")
    dpg.add_separator()

    # Paso 4: Interpretar el resultado
    dpg.add_text("Paso 4: Interpretar el resultado", tag="p4")

    ip_str = ".".join(map(str, ip))
    ip_subred = [ip[i] & mask[i] for i in range(4)]
    ip_subred_str = ".".join(map(str, ip_subred))
    dpg.add_text(
        f"El equipo con dirección IP {ip_str}/{clase} es el host {H} de la subred {ip_subred_str}/{clase_base}"
    )

    for i in range(1, 5):
        dpg.bind_item_font(f"p{i}", "bold")
        dpg.configure_item(f"p{i}", color=(0, 255, 0))


@back_func
def topic_3(sender, app_data, user_data):
    # Paso 0: Obtener los datos
    ip_base = dpg.get_value("ip")
    clase = dpg.get_value("v1")
    if clase == 0:
        clase = sum([8 if ip_base[0] < i else 0 for i in [128, 192, 224]])
        dpg.set_value("v1", clase)
    H = dpg.get_value("v2")

    # Paso 1: Pasar a binario la IP del host
    dpg.add_text("Paso 1: Pasar a binario el numero de host", tag="p1")

    ip_host = [H // 256 ** (3 - i) % 256 for i in range(4)]
    ip_host_bin = ".".join(map(lambda x: bin(x)[2:].zfill(8), ip_host))
    dpg.add_text(f"El host en binario es {ip_host_bin}")
    dpg.add_separator()

    # Paso 2: Sumar el host a la IP base
    dpg.add_text("Paso 2: Sumar el host a la IP base", tag="p2")

    ip = [ip_base[i] + ip_host[i] for i in range(4)]
    ip_bin = ".".join(map(lambda x: bin(x)[2:].zfill(8), ip))
    dpg.add_text(f"La dirección IP del host es {ip_bin}")
    dpg.add_separator()

    # Paso 3: Convertir a decimal la IP del host
    dpg.add_text("Paso 3: Convertir a decimal la IP del host", tag="p3")

    ip_str = ".".join(map(str, ip))
    dpg.add_text(f"La dirección IP del host es {ip_str}")
    dpg.add_separator()

    # Paso 4: Interpretar el resultado
    dpg.add_text("Paso 4: Interpretar el resultado", tag="p4")

    ip_base_str = ".".join(map(str, ip_base))
    dpg.add_text(
        f"El host {H} de la subred {ip_base_str}/{clase} es la dirección IP {ip_str}"
    )

    for i in range(1, 5):
        dpg.bind_item_font(f"p{i}", "bold")
        dpg.configure_item(f"p{i}", color=(0, 255, 0))


@back_func
def topic_4(sender, app_data, user_data):
    # Paso 0: Obtener los datos
    ip = dpg.get_value("ip")
    clase = dpg.get_value("v1")
    if clase == 0:
        clase = sum([8 if ip[0] < i else 0 for i in [128, 192, 224]])
        dpg.set_value("v1", clase)

    if clase % 8 == 0:
        dpg.add_text("Solo para redes sin clase", color=(255, 0, 0))
        return

    # Paso 1: Separar red y host
    dpg.add_text("Paso 1: Separar red y host", tag="p1")

    clase_base = 8 * (clase // 8)
    N = clase - clase_base
    mask = [255 if i * 8 < clase_base else 0 for i in range(4)]
    mask[clase // 8] = 256 - 2 ** (8 - N)
    mask_inv = [255 - i for i in mask]
    ip_red = [ip[i] & mask[i] for i in range(4)]
    ip_host = [ip[i] & mask_inv[i] for i in range(4)]

    ip_bin = ".".join(map(lambda x: bin(x)[2:].zfill(8), ip))
    dpg.add_text(f"La dirección IP en binario es {ip_bin}")
    ip_red_bin = ".".join(map(lambda x: bin(x)[2:].zfill(8), ip_red))
    dpg.add_text(f"La dirección IP de red en binario es {ip_red_bin}")
    ip_host_bin = ".".join(map(lambda x: bin(x)[2:].zfill(8), ip_host))
    dpg.add_text(f"La dirección IP de host en binario es {ip_host_bin}")
    dpg.add_separator()

    # Paso 2: Identificar bits de subred
    dpg.add_text("Paso 2: Identificar bits de subred", tag="p2")

    num_subred = ip_red[clase // 8] // (2 ** (8 - N)) + 1
    dpg.add_text(f"El número de subred es {num_subred}")
    dpg.add_separator()

    # Paso 3: Interpretar el resultado
    dpg.add_text("Paso 3: Interpretar el resultado", tag="p3")

    ip_str = ".".join(map(str, ip))
    ip_red_str = ".".join(map(str, ip_red))
    dpg.add_text(
        f"La dirección IP {ip_str} pertenece a la {num_subred} subred de {ip_red_str}/{clase_base}"
    )

    for i in range(1, 4):
        dpg.bind_item_font(f"p{i}", "bold")
        dpg.configure_item(f"p{i}", color=(0, 255, 0))


@back_func
def topic_5(sender, app_data, user_data):
    # Paso 0: Obtener los datos
    subred = dpg.get_value("v1")
    ip = dpg.get_value("ip")
    clase = dpg.get_value("v2")
    if clase == 0:
        clase = sum([8 if ip[0] < i else 0 for i in [128, 192, 224]])
        dpg.set_value("v2", clase)

    if clase % 8 == 0:
        dpg.add_text("Solo para redes sin clase", color=(255, 0, 0))
        return

    # Paso 1: Separar red y host
    dpg.add_text("Paso 1: Separar red y host", tag="p1")

    clase_base = 8 * (clase // 8)
    N = clase - clase_base
    mask = [255 if i * 8 < clase_base else 0 for i in range(4)]
    mask[clase // 8] = 256 - 2 ** (8 - N)
    mask_inv = [255 - i for i in mask]
    ip_red = [ip[i] & mask[i] for i in range(4)]
    ip_host = [ip[i] & mask_inv[i] for i in range(4)]

    ip_bin = ".".join(map(lambda x: bin(x)[2:].zfill(8), ip))
    dpg.add_text(f"La dirección IP en binario es {ip_bin}")
    ip_red_bin = ".".join(map(lambda x: bin(x)[2:].zfill(8), ip_red))
    dpg.add_text(f"La dirección IP de red en binario es {ip_red_bin}")
    ip_host_bin = ".".join(map(lambda x: bin(x)[2:].zfill(8), ip_host))
    dpg.add_text(f"La dirección IP de host en binario es {ip_host_bin}")
    dpg.add_separator()

    # Paso 2: Identificar bits de subred
    dpg.add_text("Paso 2: Identificar bits de subred", tag="p2")

    ip_subred = ip.copy()
    ip_subred[clase // 8] = (subred - 1) * 2 ** (8 - N)
    ip_subred_bin = ".".join(map(lambda x: bin(x)[2:].zfill(8), ip_subred))
    dpg.add_text(f"La dirección IP de la subred {subred} es {ip_subred_bin}")
    dpg.add_separator()

    # Paso 3: Convertir a decimal la IP de subred y broadcast
    dpg.add_text("Paso 3: Convertir a decimal la IP de subred y broadcast", tag="p3")

    ip_subred_str = ".".join(map(str, ip_subred))
    dpg.add_text(f"La dirección IP de subred es {ip_subred_str}")
    mask_inv = [255 - i for i in mask]
    ip_broadcast = [ip_subred[i] | mask_inv[i] for i in range(4)]
    ip_broadcast_str = ".".join(map(str, ip_broadcast))
    dpg.add_text(f"La dirección IP de broadcast es {ip_broadcast_str}")
    dpg.add_separator()

    # Paso 4: Interpretar el resultado y mostrar la tabla
    dpg.add_text("Paso 4: Interpretar el resultado", tag="p4")

    with dpg.table(
        header_row=True,
        delay_search=True,
        borders_outerH=True,
        borders_outerV=True,
        borders_innerV=True,
        no_host_extendX=True,
        row_background=True,
        policy=dpg.mvTable_SizingFixedFit,
        tag="table",
    ):
        dpg.add_table_column(label="IP Subred")
        dpg.add_table_column(label="Primer Host")
        dpg.add_table_column(label="Último Host")
        dpg.add_table_column(label="Broadcast")

        with dpg.table_row():
            dpg.add_text(ip_subred_str)
            dpg.add_text(".".join(map(str, add_ip(ip_subred.copy(), 1))))
            dpg.add_text(".".join(map(str, add_ip(ip_broadcast.copy(), -1))))
            dpg.add_text(ip_broadcast_str)

    for i in range(1, 5):
        dpg.bind_item_font(f"p{i}", "bold")
        dpg.configure_item(f"p{i}", color=(0, 255, 0))


@back_func
def topic_6(sender, app_data, user_data):
    # Paso 0: Obtener los datos
    ip = dpg.get_value("ip")
    clase = dpg.get_value("v1")
    if clase == 0:
        clase = sum([8 if ip[0] < i else 0 for i in [128, 192, 224]])
        dpg.set_value("v1", clase)
    hosts = dpg.get_value("v3")
    hosts = list(map(int, hosts.split("-")))

    # Paso 1: Ordenar los hosts
    dpg.add_text("Paso 1: Ordenar los hosts de mayor a menor", tag="p1")

    hosts.sort(reverse=True)
    dpg.add_text(f"Los hosts son {hosts}")
    dpg.add_separator()

    # Paso 2: Identificar la máscara actual
    dpg.add_text("Paso 2: Identificar la máscara actual", tag="p2")

    clase_base = 8 * (clase // 8)
    N = clase - clase_base
    mask = [255 if i * 8 < clase_base else 0 for i in range(4)]
    mask[clase // 8] = 256 - 2 ** (8 - N)
    mask_str = ".".join(map(str, mask))
    dpg.add_text(f"La máscara de red es {mask_str} / {clase}")
    mask_bin = ".".join(map(lambda x: bin(x)[2:].zfill(8), mask))
    dpg.add_text(f"Máscara de red en binario: {mask_bin}")
    dpg.add_separator()

    table_data = []

    # Loop para cada host
    for i in range(len(hosts)):
        dpg.add_text(f"Subred {i+1}", tag=f"sr_{i}")
        host = hosts[i]

        # Paso 3: Obtener número de bits del host
        dpg.add_text(f"\tPaso 3: Obtener número de bits del host {i+1}", tag=f"p3_{i}")

        M = math.ceil(math.log2(host + 2))
        dpg.add_text(f"\tBits de host: {M}")
        host_available = 2**M - 2
        dpg.add_separator()

        # Paso 4: Obtener la nueva máscara
        dpg.add_text(f"\tPaso 4: Obtener la nueva máscara {i+1}", tag=f"p4_{i}")

        clase = 32 - M
        clase_base = 8 * (clase // 8)
        N = clase - clase_base
        mask = [255 if i * 8 < clase_base else 0 for i in range(4)]
        mask[clase // 8] = 256 - 2 ** (8 - N)
        mask_str = ".".join(map(str, mask))
        mask_bin = ".".join(map(lambda x: bin(x)[2:].zfill(8), mask))
        dpg.add_text(f"\tLa nueva máscara de red es {mask_bin} / {clase}")
        dpg.add_separator()
        mask_inv = [255 - i for i in mask]
        ip_broadcast = [ip[i] | mask_inv[i] for i in range(4)]

        # Paso 5: Obtener el salto de red
        dpg.add_text(f"\tPaso 5: Obtener el salto de red {i+1}", tag=f"p5_{i}")
        X = 256 - mask[clase // 8]
        dpg.add_text(f"\tSalto de red: {X}")
        dpg.add_separator()

        # Obtener datos de la tabla
        ip_str = ".".join(map(str, ip))
        first_host = ".".join(map(str, add_ip(ip.copy(), 1)))
        last_host = ".".join(map(str, add_ip(ip_broadcast.copy(), -1)))
        broadcast = ".".join(map(str, ip_broadcast))

        table_data.append(
            [
                host_available,
                mask_str + f" / {clase}",
                ip_str,
                first_host,
                last_host,
                broadcast,
            ]
        )

        X = X * 256 ** (3 - clase // 8)
        ip = add_ip(ip, X)

    # Paso 6: Mostrar la tabla
    dpg.add_text("Paso 6: Mostrar la tabla", tag="p6")

    with dpg.table(
        header_row=True,
        delay_search=True,
        borders_outerH=True,
        borders_outerV=True,
        borders_innerV=True,
        no_host_extendX=True,
        row_background=True,
        policy=dpg.mvTable_SizingFixedFit,
        tag="table",
    ):
        dpg.add_table_column(label="N°")
        dpg.add_table_column(label="Host Sol.")
        dpg.add_table_column(label="Host Dis.")
        dpg.add_table_column(label="Máscara")
        dpg.add_table_column(label="IP Subred")
        dpg.add_table_column(label="Primer Host")
        dpg.add_table_column(label="Último Host")
        dpg.add_table_column(label="Broadcast")

        for i, data in enumerate(table_data):
            with dpg.table_row():
                dpg.add_text(str(i + 1))
                dpg.add_text(str(hosts[i]))
                dpg.add_text(str(data[0]))
                dpg.add_text(data[1])
                dpg.add_text(data[2])
                dpg.add_text(data[3])
                dpg.add_text(data[4])
                dpg.add_text(data[5])

    for i in [1, 2, 6]:
        dpg.bind_item_font(f"p{i}", "bold")
        dpg.configure_item(f"p{i}", color=(0, 255, 0))

    for i in range(len(hosts)):
        for j in [3, 4, 5]:
            dpg.bind_item_font(f"p{j}_{i}", "bold_s")
            dpg.configure_item(f"p{j}_{i}", color=(0, 150, 0))
        dpg.bind_item_font(f"sr_{i}", "bold")
        dpg.configure_item(f"sr_{i}", color=(0, 200, 0))
