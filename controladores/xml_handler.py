import xml.etree.ElementTree as ET
from modelos.dron import Dron
from modelos.invernadero import Invernadero
from modelos.planta import Planta
from modelos.plan_riego import PlanRiego
from modelos.sistema import SistemaRiego

class XMLHandler:
    @staticmethod
    def cargar_configuracion(ruta_archivo, sistema):
        sistema.limpiar_configuracion()
        tree = ET.parse(ruta_archivo)
        root = tree.getroot()

        # Cargar drones
        for dron_elem in root.find("listaDrones").findall("dron"):
            dron_id = int(dron_elem.get("id"))
            nombre = dron_elem.get("nombre")
            dron = Dron(dron_id, nombre)
            sistema.agregar_dron(dron)

        # Cargar invernaderos
        for invernadero_elem in root.find("listaInvernaderos").findall("invernadero"):
            nombre = invernadero_elem.get("nombre")
            num_hileras = int(invernadero_elem.find("numeroHileras").text)
            plantas_x_hilera = int(invernadero_elem.find("plantasXhilera").text)
            invernadero = Invernadero(nombre, num_hileras, plantas_x_hilera)

            # Cargar plantas
            for planta_elem in invernadero_elem.find("listaPlantas").findall("planta"):
                hilera = int(planta_elem.get("hilera"))
                posicion = int(planta_elem.get("posicion"))
                litros = int(planta_elem.get("litrosAgua"))
                gramos = int(planta_elem.get("gramosFertilizante"))
                tipo = planta_elem.text.strip()
                planta = Planta(hilera, posicion, litros, gramos, tipo)
                invernadero.agregar_planta(planta)

            # Asignar drones a hileras
            for asignacion in invernadero_elem.find("asignacionDrones").findall("dron"):
                dron_id = int(asignacion.get("id"))
                hilera = int(asignacion.get("hilera"))
                dron = sistema.buscar_dron_por_id(dron_id)
                if dron:
                    invernadero.asignar_dron_a_hilera(dron, hilera)

            # Cargar planes de riego
            for plan_elem in invernadero_elem.find("planesRiego").findall("plan"):
                nombre_plan = plan_elem.get("nombre")
                plan = PlanRiego(nombre_plan)
                pasos = plan_elem.text.replace(" ", "").split(",")
                for paso in pasos:
                    if paso.strip():
                        partes = paso.strip().split("-")
                        hilera = int(partes[0][1:])  # "H1" → 1
                        posicion = int(partes[1][1:])  # "P2" → 2
                        plan.agregar_paso(hilera, posicion)
                invernadero.agregar_plan_riego(plan)

            sistema.agregar_invernadero(invernadero)

    @staticmethod
    def generar_salida(ruta_salida, sistema):
        raiz = ET.Element("datosSalida")
        lista_inv = ET.SubElement(raiz, "listaInvernaderos")

        actual_inv = sistema.lista_invernaderos.primero
        while actual_inv is not None:
            inv = actual_inv.valor
            inv_elem = ET.SubElement(lista_inv, "invernadero", nombre=inv.nombre)
            planes_elem = ET.SubElement(inv_elem, "listaPlanes")

            actual_plan = inv.planes_riego.primero
            while actual_plan is not None:
                plan = actual_plan.valor
                plan_elem = ET.SubElement(planes_elem, "plan", nombre=plan.nombre)

                ET.SubElement(plan_elem, "tiempoOptimoSegundos").text = str(plan.tiempo_optimo)
                ET.SubElement(plan_elem, "aguaRequeridaLitros").text = str(plan.agua_total)
                ET.SubElement(plan_elem, "fertilizanteRequeridoGramos").text = str(plan.fertilizante_total)

                eficiencia_elem = ET.SubElement(plan_elem, "eficienciaDronesRegadores")
                actual_ef = plan.eficiencia_drones.primero
                while actual_ef is not None:
                    ef = actual_ef.valor
                    ET.SubElement(
                        eficiencia_elem, "dron",
                        nombre=ef.nombre,
                        litrosAgua=str(ef.agua),
                        gramosFertilizante=str(ef.fertilizante)
                    )
                    actual_ef = actual_ef.siguiente

                instrucciones_elem = ET.SubElement(plan_elem, "instrucciones")
                tiempo_idx = 1
                actual_tiempo = plan.instrucciones_por_tiempo.primero
                while actual_tiempo is not None:
                    lista_acciones = actual_tiempo.valor  # dict: {dron_nombre: accion}
                    tiempo_elem = ET.SubElement(instrucciones_elem, "tiempo", segundos=str(tiempo_idx))
                    for dron_nombre, accion in lista_acciones.items():
                        ET.SubElement(tiempo_elem, "dron", nombre=dron_nombre, accion=accion)
                    tiempo_idx += 1
                    actual_tiempo = actual_tiempo.siguiente

                actual_plan = actual_plan.siguiente
            actual_inv = actual_inv.siguiente

        arbol = ET.ElementTree(raiz)
        # ET.indent disponible en Python 3.9+, si falla puedes quitarlo
        try:
            ET.indent(arbol, space="    ", level=0)
        except AttributeError:
            pass
        arbol.write(ruta_salida, encoding="utf-8", xml_declaration=True)
