import xml.etree.ElementTree as ET
from modelos.dron import Dron
from modelos.invernadero import Invernadero
from modelos.planta import Planta
from modelos.plan_riego import PlanRiego
from modelos.sistema import SistemaRiego
import xml.etree.ElementTree as ET
from modelos.instruccion_tiempo import InstruccionTiempo

class XMLHandler:
    @staticmethod
    def cargar_configuracion(ruta_archivo, sistema):

        sistema.limpiar_configuracion()
        tree = ET.parse(ruta_archivo)
        root = tree.getroot()

        print("=== DEPURACIÓN: CARGANDO CONFIGURACIÓN ===")
        
        # Primero cargar todos los drones disponibles en el sistema
        drones_globales = {}
        for dron_elem in root.find("listaDrones").findall("dron"):
            dron_id = int(dron_elem.get("id"))
            nombre = dron_elem.get("nombre")
            print(f"  - Registrando dron global: ID={dron_id}, Nombre={nombre}")
            drones_globales[dron_id] = nombre

        # Cargar invernaderos
        for invernadero_elem in root.find("listaInvernaderos").findall("invernadero"):
            nombre = invernadero_elem.get("nombre")
            num_hileras = int(invernadero_elem.find("numeroHileras").text)
            plantas_x_hilera = int(invernadero_elem.find("plantasXhilera").text)
            print(f"\nCargando invernadero: {nombre}")
            print(f"  - Hileras: {num_hileras}, Plantas por hilera: {plantas_x_hilera}")
            
            invernadero = Invernadero(nombre, num_hileras, plantas_x_hilera)

            # Cargar plantas
            print("  Cargando plantas...")
            planta_count = 0
            for planta_elem in invernadero_elem.find("listaPlantas").findall("planta"):
                hilera = int(planta_elem.get("hilera"))
                posicion = int(planta_elem.get("posicion"))
                litros = int(planta_elem.get("litrosAgua"))
                gramos = int(planta_elem.get("gramosFertilizante"))
                tipo = planta_elem.text.strip()
                planta = Planta(hilera, posicion, litros, gramos, tipo)
                invernadero.agregar_planta(planta)
                planta_count += 1
            print(f"  - Total plantas cargadas: {planta_count}")

            # Asignar drones a hileras - CORREGIDO: Crear nuevas instancias
            print("  Asignando drones a hileras...")
            for asignacion in invernadero_elem.find("asignacionDrones").findall("dron"):
                dron_id = int(asignacion.get("id"))
                hilera = int(asignacion.get("hilera"))
                print(f"    - Asignando dron ID={dron_id} a hilera {hilera}")
                
                # Verificar si el dron existe en la lista global
                if dron_id in drones_globales:
                    nombre_dron = drones_globales[dron_id]
                    print(f"      ✓ Dron encontrado: {nombre_dron}")
                    
                    # Crear NUEVA instancia del dron para este invernadero
                    dron = Dron(dron_id, nombre_dron)
                    dron.asignar_a_hilera(hilera)
                    print(f"      - {dron.nombre} asignado a hilera {dron.hilera_asignada}")
                    
                    # Agregar al invernadero
                    invernadero.drones_asignados.insertar(dron)
                    print(f"      ✓ Dron {dron.nombre} agregado a drones_asignados")
                else:
                    print(f"      ❌ ERROR: No se encontró dron con ID={dron_id}")

            # Mostrar drones asignados después de cargar
            print("  Resumen de drones asignados:")
            actual_dron = invernadero.drones_asignados.primero
            count = 0
            while actual_dron is not None:
                dron = actual_dron.valor
                print(f"    {count+1}. {dron.nombre} -> Hilera {dron.hilera_asignada}")
                actual_dron = actual_dron.siguiente
                count += 1

            # Cargar planes de riego
            print("  Cargando planes de riego...")
            plan_count = 0
            for plan_elem in invernadero_elem.find("planesRiego").findall("plan"):
                nombre_plan = plan_elem.get("nombre")
                print(f"    - Plan: {nombre_plan}")
                plan = PlanRiego(nombre_plan)
                pasos = plan_elem.text.replace(" ", "").split(",")
                paso_count = 0
                for paso in pasos:
                    if paso.strip():
                        partes = paso.strip().split("-")
                        hilera = int(partes[0][1:])  # "H1" → 1
                        posicion = int(partes[1][1:])  # "P2" → 2
                        plan.agregar_paso(hilera, posicion)
                        paso_count += 1
                print(f"      Pasos cargados: {paso_count}")
                invernadero.agregar_plan_riego(plan)
                plan_count += 1
            print(f"  - Total planes cargados: {plan_count}")

            sistema.agregar_invernadero(invernadero)
            print(f"✓ Invernadero {nombre} cargado exitosamente\n")

        print("=== CONFIGURACIÓN CARGADA COMPLETAMENTE ===")

    @staticmethod
    def generar_salida(ruta_salida, sistema):
        print("=== GENERANDO ARCHIVO DE SALIDA XML ===")
        
        # Crear la estructura raíz
        raiz = ET.Element("datosSalida")
        lista_inv = ET.SubElement(raiz, "listaInvernaderos")

        # Recorrer todos los invernaderos
        actual_inv = sistema.lista_invernaderos.primero
        while actual_inv is not None:
            inv = actual_inv.valor
            print(f"Procesando invernadero: {inv.nombre}")
            
            inv_elem = ET.SubElement(lista_inv, "invernadero")
            inv_elem.set("nombre", inv.nombre)
            planes_elem = ET.SubElement(inv_elem, "listaPlanes")

            # Recorrer todos los planes del invernadero
            actual_plan = inv.planes_riego.primero
            while actual_plan is not None:
                plan = actual_plan.valor
                print(f"  Procesando plan: {plan.nombre}")
                
                plan_elem = ET.SubElement(planes_elem, "plan")
                plan_elem.set("nombre", plan.nombre)

                # Agregar estadísticas del plan
                ET.SubElement(plan_elem, "tiempoOptimoSegundos").text = str(plan.tiempo_optimo)
                ET.SubElement(plan_elem, "aguaRequeridaLitros").text = str(plan.agua_total)
                ET.SubElement(plan_elem, "fertilizanteRequeridoGramos").text = str(plan.fertilizante_total)

                # Eficiencia por dron
                eficiencia_elem = ET.SubElement(plan_elem, "eficienciaDronesRegadores")
                actual_ef = plan.eficiencia_drones.primero
                while actual_ef is not None:
                    ef = actual_ef.valor
                    dron_elem = ET.SubElement(eficiencia_elem, "dron")
                    dron_elem.set("nombre", ef.nombre)
                    dron_elem.set("litrosAgua", str(ef.agua))
                    dron_elem.set("gramosFertilizante", str(ef.fertilizante))
                    actual_ef = actual_ef.siguiente

                # Instrucciones por tiempo
                instrucciones_elem = ET.SubElement(plan_elem, "instrucciones")
                tiempo_idx = 1
                actual_tiempo = plan.instrucciones_por_tiempo.primero
                
                while actual_tiempo is not None:
                    instrucciones_lista = actual_tiempo.valor
                    tiempo_elem = ET.SubElement(instrucciones_elem, "tiempo")
                    tiempo_elem.set("segundos", str(tiempo_idx))

                    # Obtener todos los drones del invernadero para este plan
                    drones_inv = []
                    actual_dron_inv = inv.drones_asignados.primero
                    while actual_dron_inv is not None:
                        drones_inv.append(actual_dron_inv.valor.nombre)
                        actual_dron_inv = actual_dron_inv.siguiente

                    # Para cada dron, buscar su instrucción en este tiempo
                    for dron_nombre in drones_inv:
                        accion = "Esperar"  # Valor por defecto
                        actual_inst = instrucciones_lista.primero
                        while actual_inst is not None:
                            instruccion = actual_inst.valor
                            if instruccion.nombre_dron == dron_nombre:
                                accion = instruccion.accion
                                break
                            actual_inst = actual_inst.siguiente
                        
                        dron_inst_elem = ET.SubElement(tiempo_elem, "dron")
                        dron_inst_elem.set("nombre", dron_nombre)
                        dron_inst_elem.set("accion", accion)

                    tiempo_idx += 1
                    actual_tiempo = actual_tiempo.siguiente

                actual_plan = actual_plan.siguiente
            actual_inv = actual_inv.siguiente

        # Crear el árbol XML y guardar
        arbol = ET.ElementTree(raiz)
        
        # Intentar formatear el XML (disponible en Python 3.9+)
        try:
            ET.indent(arbol, space="    ", level=0)
        except AttributeError:
            print("  ⚠️  ET.indent no disponible (Python < 3.9), XML sin formato")
            pass

        # Escribir el archivo
        arbol.write(ruta_salida, encoding="utf-8", xml_declaration=True)
        print(f"✓ Archivo de salida generado: {ruta_salida}")
        return True