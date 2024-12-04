# Definir los colores
colores = {
    "Bright Red": "\033[91m",
    "Bright Green": "\033[92m",
    "Bright Yellow": "\033[93m",
    "Bright Blue": "\033[94m",
    "Bright Cyan": "\033[96m",
    "Reset": "\033[0m",
}


def obtener_transicion(transiciones, estado, simbolo):
    return transiciones[estado][simbolo]


def analizar_transiciones(datos_entrada, encabezados):
    # Esta función analiza los datos de entrada para crear una tabla de transiciones
    # que será usada posteriormente en el proceso de minimización del DFA.

    # 'lineas' es una lista que contiene cada línea de la cadena 'datos_entrada',
    # eliminando los espacios en blanco al principio y al final de la cadena.
    lineas = datos_entrada.strip().split("\n")

    # 'transiciones' es una lista de listas que se inicializa con listas vacías.
    # La cantidad de listas vacías es igual al número de líneas en 'lineas'.
    # Cada sublista en 'transiciones' representará las transiciones de un estado.
    transiciones = [[] for _ in range(len(lineas))]

    # Se itera sobre cada 'linea' en 'lineas'.
    for linea in lineas:
        # 'valores' es una lista de enteros que se obtiene al separar la 'linea'
        # en componentes individuales (usando espacios como separadores) y luego
        # convertir esos componentes en números enteros.
        valores = list(map(int, linea.split()))

        # 'estado' es el primer valor de 'valores' y representa el estado actual
        # en el que se encuentra el autómata.
        estado = valores[0]

        # La sublista en 'transiciones' correspondiente al 'estado' actual se llena
        # con los valores restantes en 'valores', que representan los estados a los
        # que se transita desde el estado actual para cada símbolo en el alfabeto.
        # Por ejemplo, si 'valores' es [0, 1, 2], esto indica que el estado 0
        # transita al estado 1 con el primer símbolo del alfabeto y al estado 2
        # con el segundo símbolo.
        transiciones[estado] = valores[1:]

    # La función devuelve la tabla de 'transiciones', que es una lista de listas
    # donde cada sublista representa las transiciones de un estado específico.
    return transiciones


def minimizar_dfa(estados, alfabeto, transiciones, estados_aceptacion):
    # Esta función minimiza un autómata finito determinista (DFA) eliminando
    # estados equivalentes y agrupándolos en clases de equivalencia.

    # 'pares' es una lista de todas las combinaciones posibles de pares de estados
    # (p, q) donde p < q. Estos pares se usarán para verificar la equivalencia
    # de los estados.
    pares = [(p, q) for p in estados for q in estados if p < q]

    # 'marcados' es un conjunto que almacenará los pares de estados que se han
    # determinado como no equivalentes.
    marcados = set()

    # Se marca un par (p, q) si uno de los estados es de aceptación y el otro no lo es.
    for p, q in pares:
        if (p in estados_aceptacion) != (q in estados_aceptacion):
            marcados.add((p, q))

    # Este bucle refina la tabla de pares de estados marcando aquellos pares que
    # no son equivalentes, con base en las transiciones.
    cambios = True
    while cambios:
        cambios = False
        nuevos_marcados = set(marcados)
        for p, q in pares:
            # Si el par ya está marcado, se salta al siguiente.
            if (p, q) in marcados:
                continue
            # Se verifica para cada símbolo en el alfabeto si las transiciones
            # de p y q llevan a pares de estados que ya están marcados.
            for simbolo in range(len(alfabeto)):
                p_siguiente = obtener_transicion(transiciones, p, simbolo)
                q_siguiente = obtener_transicion(transiciones, q, simbolo)
                # Si las transiciones desde p y q llevan a estados que forman un
                # par ya marcado, se marca el par (p, q) también.
                if (p_siguiente, q_siguiente) in marcados or (
                    q_siguiente,
                    p_siguiente,
                ) in marcados:
                    nuevos_marcados.add((p, q))
                    cambios = True
                    break
        marcados = nuevos_marcados

    # Aquí se agrupan los estados que no están marcados como no equivalentes
    # en clases de equivalencia.
    clases_equivalencia = []
    for p, q in pares:
        if (p, q) not in marcados:
            clases_equivalencia.append((p, q))

    # La función devuelve una lista de pares de estados que son equivalentes.
    return clases_equivalencia


def eliminar_estados_inalcanzables(estados, alfabeto, transiciones, estado_inicial):
    # Esta función identifica y devuelve un conjunto de estados alcanzables
    # a partir del 'estado_inicial'. Los estados inalcanzables serán excluidos.

    # 'alcanzables' es un conjunto que almacenará todos los estados que son alcanzables
    # desde el 'estado_inicial'.
    alcanzables = set()

    # 'cola' es una lista que actúa como una cola para realizar una búsqueda en
    # amplitud (BFS). Inicialmente, contiene solo el 'estado_inicial'.
    cola = [estado_inicial]

    # Mientras haya estados en la 'cola', se sigue buscando.
    while cola:
        # 'estado' toma el primer elemento de la 'cola', y este es removido.
        estado = cola.pop(0)

        # Si 'estado' aún no está en 'alcanzables', se agrega.
        if estado not in alcanzables:
            alcanzables.add(estado)

            # Iterar sobre todos los símbolos en el 'alfabeto'.
            for simbolo in range(len(alfabeto)):
                # Obtener el estado al que se transita desde 'estado' con el 'simbolo' actual.
                estado_siguiente = obtener_transicion(transiciones, estado, simbolo)

                # Si el 'estado_siguiente' aún no es alcanzable, se agrega a la 'cola'
                # para continuar explorando desde allí.
                if estado_siguiente not in alcanzables:
                    cola.append(estado_siguiente)

    # La función devuelve el conjunto 'alcanzables', que contiene todos los estados
    # que se pueden alcanzar desde el 'estado_inicial'.
    return alcanzables


def main():
    with open("input.txt", "r") as archivo:
        datos = archivo.read().strip().split("\n")

    casos_prueba = int(datos[0])
    indice = 1
    resultados = []

    for i in range(casos_prueba):
        color_actual = list(colores.values())[
            i % (len(colores) - 1)
        ]  # Exclude "Reset" from cycling colors

        print(f"{color_actual}Case {i + 1}:{colores['Reset']}")

        estados_n = int(datos[indice])
        indice += 1
        alfabeto = datos[indice].split()
        indice += 1
        estados_aceptacion = set(map(int, datos[indice].split()))
        indice += 1

        transiciones = ""
        for _ in range(estados_n):
            transiciones += datos[indice] + "\n"
            indice += 1

        transiciones = analizar_transiciones(transiciones, alfabeto)

        estado_inicial = 0
        estados = set(range(estados_n))

        # Eliminar estados inalcanzables
        estados_alcanzables = eliminar_estados_inalcanzables(
            estados, alfabeto, transiciones, estado_inicial
        )

        # Minimizar DFA
        clases_equivalencia = minimizar_dfa(
            estados_alcanzables, alfabeto, transiciones, estados_aceptacion
        )

        # Imprimir las clases de equivalencia con el color actual
        for p, q in clases_equivalencia:
            print(f"{color_actual}({p}, {q}){colores['Reset']}", end=" ")
        print("\n")  # Espacio adicional entre casos


if __name__ == "__main__":
    main()
