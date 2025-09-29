# controladores/simulador.py
from estructuras.cola import Cola
from estructuras.lista_simple import ListaSimple
from modelos.instruccion_tiempo import InstruccionTiempo

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

        # reiniciar estado de drones
        actual_dron = invernadero.drones_asignados.primero
        while actual_dron is not None:
            dron = actual_dron.valor
            dron.posicion_actual = 0  # empiezan en posición 0 (antes de la primera planta)
            dron.total_agua = 0
            dron.total_fertilizante = 0
            dron.instrucciones = ListaSimple()
            actual_dron = actual_dron.siguiente

        # crear cola de operaciones pendientes
        cola_riegos = Cola()
        actual_paso = plan.orden_riego.primero
        while actual_paso is not None:
            cola_riegos.encolar(actual_paso.valor)
            actual_paso = actual_paso.siguiente

        tiempo = 0
        instrucciones_globales = ListaSimple()

        # mmientras haya riegos pendientes
        while not cola_riegos.esta_vacia():
            tiempo += 1
            instrucciones_tiempo = ListaSimple()

            # obtener el proximo riego sin desencolar todavía
            siguiente_riego = cola_riegos.ver_frente()
            if siguiente_riego is None:
                break

            hilera_objetivo, posicion_objetivo = siguiente_riego

            # encontrar dron asignado a la hilera objetivo
            dron_objetivo = None
            actual_dron = invernadero.drones_asignados.primero
            while actual_dron is not None:
                dron = actual_dron.valor
                if dron.hilera_asignada == hilera_objetivo:
                    dron_objetivo = dron
                    break
                actual_dron = actual_dron.siguiente

            if not dron_objetivo:
                # si no hay dron para esa hilera descartamos este paso
                cola_riegos.desencolar()
                continue

            # procesar cada dron
            actual_dron = invernadero.drones_asignados.primero
            riego_realizado = False
            
            while actual_dron is not None:
                dron = actual_dron.valor
                accion = "Esperar"

                if dron == dron_objetivo:
                    # este dron es el encargado del proximo riego
                    if dron.posicion_actual == posicion_objetivo:
                        # si esta en la posición correcta regar
                        planta = invernadero.obtener_planta(hilera_objetivo, posicion_objetivo)
                        if planta:
                            dron.total_agua += planta.litros_agua
                            dron.total_fertilizante += planta.gramos_fertilizante
                            accion = "Regar"
                            cola_riegos.desencolar()  # eliminar este riego de la cola
                            riego_realizado = True
                    elif dron.posicion_actual < posicion_objetivo:
                        # necesita avanzar
                        dron.posicion_actual += 1
                        accion = f"Adelante (H{dron.hilera_asignada}P{dron.posicion_actual})"
                    else:
                        # necesita retroceder
                        dron.posicion_actual -= 1
                        accion = f"Atrás (H{dron.hilera_asignada}P{dron.posicion_actual})"
                else:
                    # este dron no es el encargado del proximo riego
                    # buscar si tiene algún riego pendiente en su hilera
                    objetivo_local = self._buscar_proximo_objetivo_dron(dron, cola_riegos)
                    
                    if objetivo_local is not None:
                        if dron.posicion_actual < objetivo_local:
                            dron.posicion_actual += 1
                            accion = f"Adelante (H{dron.hilera_asignada}P{dron.posicion_actual})"
                        elif dron.posicion_actual > objetivo_local:
                            dron.posicion_actual -= 1
                            accion = f"Atrás (H{dron.hilera_asignada}P{dron.posicion_actual})"
                        else:
                            accion = "Esperar"
                    else:
                        # no tiene riegos pendientes, regresar al inicio
                        if dron.posicion_actual > 0:
                            dron.posicion_actual -= 1
                            accion = f"Atrás (H{dron.hilera_asignada}P{dron.posicion_actual})"
                        else:
                            accion = "Esperar"

                # crear y agregar instruccion
                instruccion = InstruccionTiempo(dron.nombre, accion)
                instrucciones_tiempo.insertar(instruccion)
                actual_dron = actual_dron.siguiente

            # agregar las instrucciones de este tiempo
            instrucciones_globales.insertar(instrucciones_tiempo)

        # guardar resultados en el plan
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

        print(f"    Simulación completada: {plan.nombre}")
        print(f"    - Tiempo óptimo: {plan.tiempo_optimo} segundos")
        print(f"    - Agua total: {plan.agua_total} litros") 
        print(f"    - Fertilizante total: {plan.fertilizante_total} gramos")
        print(f"    - Instrucciones generadas: {instrucciones_globales.tamanio} tiempos")

        # guardar instrucciones en el plan
        actual_inst = instrucciones_globales.primero
        while actual_inst is not None:
            plan.agregar_tiempo_instrucciones(actual_inst.valor)
            actual_inst = actual_inst.siguiente

        return True

    def _buscar_proximo_objetivo_dron(self, dron, cola_riegos):
        """busca el próximo objetivo para un dron específico en la cola de riegos"""
        # crear cola temporal para buscar sin modificar la original
        cola_temp = Cola()
        objetivo = None
        
        # bbuscar en la cola el primer riego para la hilera de este dron
        encontrado = False
        while not cola_riegos.esta_vacia():
            item = cola_riegos.desencolar()
            cola_temp.encolar(item)
            if not encontrado and item[0] == dron.hilera_asignada:
                objetivo = item[1]
                encontrado = True
        
        # rrestaurar cola original
        while not cola_temp.esta_vacia():
            cola_riegos.encolar(cola_temp.desencolar())
            
        return objetivo