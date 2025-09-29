import xml.etree.ElementTree as ET
from modelos.dron import Dron
from modelos.invernadero import Invernadero
from modelos.planta import Planta
from modelos.plan_riego import PlanRiego
from modelos.sistema import SistemaRiego
from modelos.instruccion_tiempo import InstruccionTiempo
from estructuras.lista_simple import ListaSimple

class DronRegistro:
    def __init__(self, id_, nombre):
        self.id = id_
        self.nombre = nombre

class XMLHandler:
    @staticmethod
    def cargar_configuracion(ruta_archivo, sistema):

        sistema.limpiar_configuracion()
        tree = ET.parse(ruta_archivo)
        root = tree.getroot()

        print("=== DEPURACIÓN: CARGANDO CONFIGURACIÓN ===")
        
        # Primero cargar todos los drones disponibles en el sistema (usando ListaSimple)
        drones_globales = ListaSimple()
        lista_drones_elem = root.find("listaDrones")
        if lista_drones_elem is not None:
            for dron_elem in lista_drones_elem.findall("dron"):
                dron_id = int(dron_elem.get("id"))
                nombre = dron_elem.get("nombre")
                print(f"  - Registrando dron global: ID={dron_id}, Nombre={nombre}")
                drones_globales.insertar(DronRegistro(dron_id, nombre))

        # Cargar invernaderos
        lista_invernaderos_elem = root.find("listaInvernaderos")
        if lista_invernaderos_elem is None:
            print("  ⚠️ No se encontró <listaInvernaderos> en el XML.")
            return False

        for invernadero_elem in lista_invernaderos_elem.findall("invernadero"):
            nombre = invernadero_elem.get("nombre")
            num_hileras = int(invernadero_elem.find("numeroHileras").text)
            plantas_x_hilera = int(invernadero_elem.find("plantasXhilera").text)
            print(f"\nCargando invernadero: {nombre}")
            print(f"  - Hileras: {num_hileras}, Plantas por hilera: {plantas_x_hilera}")
            
            invernadero = Invernadero(nombre, num_hileras, plantas_x_hilera)

            # Cargar plantas
            print("  Cargando plantas...")
            planta_count = 0
            lista_plantas_elem = invernadero_elem.find("listaPlantas")
            if lista_plantas_elem is not None:
                for planta_elem in lista_plantas_elem.findall("planta"):
                    hilera = int(planta_elem.get("hilera"))
                    posicion = int(planta_elem.get("posicion"))
                    litros = int(planta_elem.get("litrosAgua"))
                    gramos = int(planta_elem.get("gramosFertilizante"))
                    tipo = planta_elem.text.strip() if planta_elem.text else ""
                    planta = Planta(hilera, posicion, litros, gramos, tipo)
                    invernadero.agregar_planta(planta)
                    planta_count += 1
            print(f"  - Total plantas cargadas: {planta_count}")

            # Asignar drones a hileras (buscar en drones_globales usando ListaSimple)
            print("  Asignando drones a hileras...")
            asignaciones_elem = invernadero_elem.find("asignacionDrones")
            if asignaciones_elem is not None:
                for asignacion in asignaciones_elem.findall("dron"):
                    dron_id = int(asignacion.get("id"))
                    hilera = int(asignacion.get("hilera"))
                    print(f"    - Asignando dron ID={dron_id} a hilera {hilera}")

                    # buscar en drones_globales
                    nombre_dron = None
                    actual_reg = drones_globales.primero
                    while actual_reg is not None:
                        reg = actual_reg.valor
                        if reg.id == dron_id:
                            nombre_dron = reg.nombre
                            break
                        actual_reg = actual_reg.siguiente

                    if nombre_dron is not None:
                        print(f"      ✓ Dron encontrado: {nombre_dron}")
                        dron = Dron(dron_id, nombre_dron)
                        dron.asignar_a_hilera(hilera)
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

            # Cargar planes de riego (PARSER manual, sin usar split ni listas literales)
            print("  Cargando planes de riego...")
            plan_count = 0
            planes_elem = invernadero_elem.find("planesRiego")
            if planes_elem is not None:
                for plan_elem in planes_elem.findall("plan"):
                    nombre_plan = plan_elem.get("nombre")
                    print(f"    - Plan: {nombre_plan}")
                    plan = PlanRiego(nombre_plan)

                    texto_pasos = plan_elem.text if plan_elem.text else ""
                    texto_pasos = texto_pasos.strip()
                    paso = ""
                    paso_count = 0

                    def procesar_paso(paso_cadena):
                        # devuelve (hilera, posicion) analizado sin usar slicing con []
                        hilera = 0
                        posicion = 0
                        leyendo = None  # 'hilera' o 'pos'
                        numero = ""
                        for ch in paso_cadena:
                            if ch == "H" or ch == "h":
                                leyendo = "hilera"
                                numero = ""
                            elif ch == "P" or ch == "p":
                                # si había un número en lectura anterior, lo asignamos
                                if leyendo == "hilera" and numero != "":
                                    try:
                                        hilera = int(numero)
                                    except Exception:
                                        hilera = 0
                                leyendo = "pos"
                                numero = ""
                            elif ch.isdigit():
                                numero += ch
                            elif ch == "-" or ch == " ":
                                if numero != "":
                                    try:
                                        if leyendo == "hilera":
                                            hilera = int(numero)
                                        elif leyendo == "pos":
                                            posicion = int(numero)
                                    except Exception:
                                        pass
                                    numero = ""
                                # separador: ignorar
                            else:
                                # ignorar otros caracteres
                                pass
                        # al final, si quedó número, asignarlo según último modo de lectura
                        if numero != "":
                            try:
                                if leyendo == "hilera":
                                    hilera = int(numero)
                                elif leyendo == "pos":
                                    posicion = int(numero)
                            except Exception:
                                pass
                        return hilera, posicion

                    for caracter in texto_pasos:
                        if caracter == ",":
                            paso = paso.strip()
                            if paso != "":
                                h, p = procesar_paso(paso)
                                if h > 0 and p > 0:
                                    plan.agregar_paso(h, p)
                                    paso_count += 1
                            paso = ""
                        else:
                            paso += caracter

                    # último paso si no termina en coma
                    paso = paso.strip()
                    if paso != "":
                        h, p = procesar_paso(paso)
                        if h > 0 and p > 0:
                            plan.agregar_paso(h, p)
                            paso_count += 1

                    print(f"      Pasos cargados: {paso_count}")
                    invernadero.agregar_plan_riego(plan)
                    plan_count += 1
            print(f"  - Total planes cargados: {plan_count}")

            sistema.agregar_invernadero(invernadero)
            print(f"✓ Invernadero {nombre} cargado exitosamente\n")

        print("=== CONFIGURACIÓN CARGADA COMPLETAMENTE ===")
        return True

    @staticmethod
    def generar_salida(ruta_salida, sistema):
        print("=== GENERANDO ARCHIVO DE SALIDA XML ===")
        
        raiz = ET.Element("datosSalida")
        lista_inv = ET.SubElement(raiz, "listaInvernaderos")

        actual_inv = sistema.lista_invernaderos.primero
        while actual_inv is not None:
            inv = actual_inv.valor
            print(f"Procesando invernadero: {inv.nombre}")
            
            inv_elem = ET.SubElement(lista_inv, "invernadero")
            inv_elem.set("nombre", inv.nombre)
            planes_elem = ET.SubElement(inv_elem, "listaPlanes")

            actual_plan = inv.planes_riego.primero
            while actual_plan is not None:
                plan = actual_plan.valor
                print(f"  Procesando plan: {plan.nombre}")
                
                plan_elem = ET.SubElement(planes_elem, "plan")
                plan_elem.set("nombre", plan.nombre)

                ET.SubElement(plan_elem, "tiempoOptimoSegundos").text = str(plan.tiempo_optimo)
                ET.SubElement(plan_elem, "aguaRequeridaLitros").text = str(plan.agua_total)
                ET.SubElement(plan_elem, "fertilizanteRequeridoGramos").text = str(plan.fertilizante_total)

                eficiencia_elem = ET.SubElement(plan_elem, "eficienciaDronesRegadores")
                actual_ef = plan.eficiencia_drones.primero
                while actual_ef is not None:
                    ef = actual_ef.valor
                    dron_elem = ET.SubElement(eficiencia_elem, "dron")
                    dron_elem.set("nombre", ef.nombre)
                    dron_elem.set("litrosAgua", str(ef.agua))
                    dron_elem.set("gramosFertilizante", str(ef.fertilizante))
                    actual_ef = actual_ef.siguiente

                instrucciones_elem = ET.SubElement(plan_elem, "instrucciones")
                tiempo_idx = 1
                actual_tiempo = plan.instrucciones_por_tiempo.primero
                while actual_tiempo is not None:
                    instrucciones_lista = actual_tiempo.valor
                    tiempo_elem = ET.SubElement(instrucciones_elem, "tiempo")
                    tiempo_elem.set("segundos", str(tiempo_idx))

                    # Iterar directamente la lista de drones del invernadero (sin crear listas Python)
                    actual_dron_inv = inv.drones_asignados.primero
                    while actual_dron_inv is not None:
                        dron_nombre = actual_dron_inv.valor.nombre
                        accion = "Esperar"
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

                        actual_dron_inv = actual_dron_inv.siguiente

                    tiempo_idx += 1
                    actual_tiempo = actual_tiempo.siguiente

                actual_plan = actual_plan.siguiente
            actual_inv = actual_inv.siguiente

        arbol = ET.ElementTree(raiz)
        try:
            ET.indent(arbol, space="    ", level=0)
        except AttributeError:
            print("  ⚠️  ET.indent no disponible (Python < 3.9), XML sin formato")
            pass

        arbol.write(ruta_salida, encoding="utf-8", xml_declaration=True)
        print(f"✓ Archivo de salida generado: {ruta_salida}")
        return True
