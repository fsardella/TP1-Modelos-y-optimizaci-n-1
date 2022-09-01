PATH = "enunciado.txt"
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


def encontrar_compatibilidades(cant_prendas, incompatibilidades):
    compatibilidades = {}
    prendas = list(range(1, cant_prendas + 1))
    for prenda in prendas:
        # lista_completa.remove(incompatibilidades[n])
        # compatibles = list(filter(lambda n_prenda: n_prenda not in incompatibilidades[prenda] and n_prenda != prenda, prendas))
        compatibles = [n_prenda for n_prenda in prendas if n_prenda not in incompatibilidades[prenda] and n_prenda != prenda]
        compatibilidades[prenda] = compatibles
    return compatibilidades

def esta_en_lavado(lavados, prenda):
    for prendas in lavados.values():
        if prenda in prendas:
            return True
    return False


def obtener_nro_lavado(lavados, prenda):
    for nro_lavado, prendas in lavados.items():
        if prenda in prendas:
            return nro_lavado

def armar_lavados(prendas, compatibilidades):
    '''Esta sería una primera versión donde se van agregando prendas según compatibilidad. Se
    analizan las prendas por tiempo descendiente y se van agrando sus compatibles. Si una prenda
    ya estaba no se analiza más'''
    lavados = {}
    i = 1
    for prenda in prendas:
        if esta_en_lavado(lavados, prenda):
            continue
        no_estan_en_lavado = [nro_prenda for nro_prenda in compatibilidades[prenda] if (esta_en_lavado(lavados, nro_prenda) == False)]
        lavados[i] = no_estan_en_lavado + [prenda]
        i += 1
    return lavados

def armar_lavados_v2(prendas, compatibilidades):
    '''Esta sería una primera versión donde se van agregando prendas según compatibilidad. Se
    analizan las prendas por tiempo descendiente y se van agrando sus compatibles. Si una prenda
    ya estaba no se analiza más'''
    lavados = {}
    i = 1
    for prenda in prendas:
        no_estan_en_lavado = [nro_prenda for nro_prenda in compatibilidades[prenda] if (esta_en_lavado(lavados, nro_prenda) == False)]
        if esta_en_lavado(lavados, prenda):
            if len(no_estan_en_lavado) == 0:
                # Si todas las prendas que son compatibles a la misma ya están en un
                # lavado continue. Esto se debe a que como se analizan las prendas
                # con tiempos de lavado descendente, si ya esta en un lavado, este
                # será uno que ocupe más tiempo.
                continue
            lavados[i] = no_estan_en_lavado + [prenda]
            n_lavado = obtener_nro_lavado(lavados, prenda)
            lavados[n_lavado].remove(prenda) # lo saco de su lavado original
            i += 1
            continue
        lavados[i] = no_estan_en_lavado + [prenda]
        i += 1
    return lavados

def chequear_tiempos(lavados, tiempos):
    tiempo_total = 0
    for n, prendas in lavados.items():
        tiempo_max = 0
        for prenda in prendas:
            tiempo = tiempos[prenda]
            if tiempo > tiempo_max:
                tiempo_max = tiempo
        tiempo_total += tiempo_max
    return tiempo_total

def cargar_resultado(lavados):
    with open("solucion_1.txt", "w") as archivo:
        for n_lavado, prendas in lavados.items():
            for prenda in prendas:
                archivo.write(f"{prenda} {n_lavado}\n")

def main():
    cant_prendas, incompatibilidades, tiempos = obtener_datos_enunciado()
    compatibilidades = encontrar_compatibilidades(cant_prendas, incompatibilidades)


    # ordeno las prendas por orden de lavado descendente
    sortedTiempos = sorted(tiempos.items(), key=lambda x: x[1])
    valores = []
    for prenda, tiempo in sortedTiempos:
        valores.append(prenda)
    valores = valores[::-1]

    print(f"valores {valores}")

    print("lavados v1")
    lavados1 = armar_lavados(valores, compatibilidades)
    print(f"lavados 1 {lavados1}")
    print(f"lavados 1 {chequear_tiempos(lavados1, tiempos)}")

    print("voy a armar lavados v2")
    lavados2 = armar_lavados_v2(valores, compatibilidades)
    print(f"lavados 2 {lavados2}")
    print(f"lavados 2 {chequear_tiempos(lavados2, tiempos)}")

    cargar_resultado(lavados2)

main()