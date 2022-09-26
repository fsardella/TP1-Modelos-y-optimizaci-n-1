PATH = "enunciado_2.txt"
ENUNCIADO = "p"
COMENTARIO = "c"
INCOMPATIBILIDAD = "e"
TIEMPO = "n"

def obtener_datos_enunciado():
    cant_prendas = 0
    incompatibilidades = {}
    tiempos = {}
    with open(PATH) as archivo:
        for linea in archivo:
            if linea[0] == ENUNCIADO:
                caracter, comantario, prendas, incop = linea.split()
                cant_prendas = int(prendas)
            elif linea[0] == INCOMPATIBILIDAD:
                caracter, prenda1, prenda2 = linea.split()
                incompatibilidades[int(prenda1)] = incompatibilidades.get(int(prenda1), []) + [int(prenda2)]
            elif linea[0] == TIEMPO:
                caracter, prenda, tiempo = linea.split()
                tiempos[int(prenda)] = int(tiempo)
    return cant_prendas, incompatibilidades, tiempos

def chequear_incompatibilidad(prenda1, prenda2, incompatibilidades):
    return (prenda1 in incompatibilidades.keys() and prenda2 in incompatibilidades[prenda1]) or (prenda2 in incompatibilidades.keys() and prenda1 in incompatibilidades[prenda2])

def armar_lavados(prendas, incompatibilidades):
    ''' Recibe una lista de prendas y un diccionario que tiene como clave
        el número de una prenda y como valor una lista con las prendas
        incompatibles a la misma.
        Devuelve un diccionario que tiene como clave el número de lavado y
        como valor una lista con todas las prendas que entran en el mismo
        (teniendo en cuenta las restricciones dadas por las incompatibilidades).'''
    lavados = {}
    i = 0
    for prenda in prendas:
        if len(lavados) == 0:  # si no había ninguna prenda para lavar, no analizo restricciones
            lavados[i] = [prenda]
            i += 1
            continue
        for n_lavado, prendas_lavado in lavados.items():
            agregar_prenda = True
            for prenda_lavado in prendas_lavado:
                if chequear_incompatibilidad(prenda_lavado, prenda, incompatibilidades):
                    # si en el lavado hay una prenda incompatible no se puede agregar al mismo
                    agregar_prenda = False
            if agregar_prenda:
                lavados[n_lavado] += [prenda]
                break
        if not agregar_prenda:
            # no pudo formar parte de ningún lavado existente, creamos uno nuevo
            lavados[i] = [prenda]
            i += 1
    return lavados

def chequear_tiempos(lavados, tiempos):
    tiempo_total = 0
    for prendas in lavados.values():
        tiempo_max = 0
        for prenda in prendas:
            tiempo = tiempos[prenda]
            if tiempo > tiempo_max:
                tiempo_max = tiempo
        tiempo_total += tiempo_max
    return tiempo_total

def cargar_resultado(lavados):
    with open("solucion_2.txt", "w") as archivo:
        for n_lavado, prendas in lavados.items():
            for prenda in prendas:
                archivo.write(f"{prenda} {n_lavado}\n")

def main():
    cant_prendas, incompatibilidades, tiempos = obtener_datos_enunciado()

    # ordeno las prendas por orden de tiempo de lavado descendente
    tiempos_ordenados = sorted(tiempos.items(), key=lambda x: x[1])
    prendas_ordenadas = []
    for prenda, tiempo in tiempos_ordenados:
        prendas_ordenadas.append(prenda)
    prendas_ordenadas = prendas_ordenadas[::-1]
    
    print(f"prendas = {prendas_ordenadas}")

    lavados_ordenados = armar_lavados(prendas_ordenadas, incompatibilidades)
    print(f"El lavado ordenado tarda {chequear_tiempos(lavados_ordenados, tiempos)}")


    print()
    print()
    print()
    print(lavados_ordenados)
    cargar_resultado(lavados_ordenados)

main()