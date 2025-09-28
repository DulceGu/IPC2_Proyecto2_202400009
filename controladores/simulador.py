from estructuras.cola import Cola
from estructuras.lista_simple import ListaSimple

class Simulador:
    def __init__(self, sistema):
        self.sistema = sistema

    def simular_plan(self, nombre_invernadero, nombre_plan):
        invernadero = self.sistema.buscar_invernadero_por_nombre(nombre_invernadero)
        if not invernadero:
            return False
        plan = invernadero.buscar_plan_por_nombre(nombre_plan)
        if not plan:
            return False

        # Reiniciar estado de drones
        actual_dron = invernadero.drones_asignados.primero
        while actual_dron is not None:
            dron = actual_dron.valor
            dron.posicion_actual = 0
            dron.total_agua = 0
            dron.total_fertilizante = 0
            dron.instrucciones = ListaSimple()
            actual_dron = actual_dron.siguiente

        # Crear cola de operaciones pendientes (copia de plan.orden_riego)
        cola_riegos = Cola()
        actual_paso = plan.orden_riego.primero
        while actual_paso is not None:
            cola_riegos.encolar(actual_paso.valor)
            actual_paso = actual_paso.siguiente

        tiempo = 0
        instrucciones_globales = []

        # Simulación por segundos hasta vaciar la cola
        while not cola_riegos.esta_vacia():
            tiempo += 1
            instrucciones_tiempo = {}

            # Obtener el riego que sigue (sin desencolar aún)
            siguiente_riego = cola_riegos.ver_frente()
            if siguiente_riego is None:
                break

            hilera_objetivo, posicion_objetivo = siguiente_riego

            # Encontrar dron asignado a la hilera objetivo
            dron_objetivo = invernadero.obtener_dron_por_hilera(hilera_objetivo)
            if not dron_objetivo:
                # Si no hay dron para esa hilera, descartamos ese paso
                cola_riegos.desencolar()
                continue

            # Para facilitar decisiones, volcar cola a lista (sin perderla)
            temp_cola = Cola()
            items = []
            while not cola_riegos.esta_vacia():
                item = cola_riegos.desencolar()
                items.append(item)
                temp_cola.encolar(item)
            # restaurar cola
            cola_riegos = temp_cola

            # Mover / accionar cada dron
            actual_dron = invernadero.drones_asignados.primero
            while actual_dron is not None:
                dron = actual_dron.valor
                accion = "Esperar"

                # Si es el dron encargado del riego actual y está en la posición -> regar
                if dron == dron_objetivo and dron.posicion_actual == posicion_objetivo:
                    planta = invernadero.obtener_planta(hilera_objetivo, posicion_objetivo)
                    if planta:
                        dron.total_agua += planta.litros_agua
                        dron.total_fertilizante += planta.gramos_fertilizante
                        accion = "Regar"
                        # quitar ese riego de la cola (ya atendido)
                        cola_riegos.desencolar()
                else:
                    # buscar primer pendiente en su hilera (si existe)
                    objetivo = None
                    for it in items:
                        if it[0] == dron.hilera_asignada:
                            objetivo = it[1]
                            break
                    if objetivo is None:
                        objetivo = 0  # regresar al inicio o esperar

                    if dron.posicion_actual < objetivo:
                        dron.posicion_actual += 1
                        accion = f"Adelante(H{dron.hilera_asignada}P{dron.posicion_actual})"
                    elif dron.posicion_actual > objetivo:
                        dron.posicion_actual -= 1
                        accion = f"Atrás(H{dron.hilera_asignada}P{dron.posicion_actual})"
                    else:
                        accion = "Esperar"

                instrucciones_tiempo[dron.nombre] = accion
                actual_dron = actual_dron.siguiente

            # Asegurar que todos los drones estén presentes en el dict
            actual_dron = invernadero.drones_asignados.primero
            while actual_dron is not None:
                dron = actual_dron.valor
                if dron.nombre not in instrucciones_tiempo:
                    instrucciones_tiempo[dron.nombre] = "Esperar"
                actual_dron = actual_dron.siguiente

            instrucciones_globales.append(instrucciones_tiempo)

        # Guardar resultados en el plan
        plan.tiempo_optimo = tiempo
        plan.agua_total = 0
        plan.fertilizante_total = 0
        actual_dron = invernadero.drones_asignados.primero
        while actual_dron is not None:
            dron = actual_dron.valor
            plan.agua_total += dron.total_agua
            plan.fertilizante_total += dron.total_fertilizante
            plan.agregar_eficiencia(dron.nombre, dron.total_agua, dron.total_fertilizante)
            actual_dron = actual_dron.siguiente

        for inst in instrucciones_globales:
            plan.agregar_tiempo_instrucciones(inst)

        return True
