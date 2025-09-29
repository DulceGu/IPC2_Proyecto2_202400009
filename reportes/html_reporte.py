
import os

class HTMLReporte:
    @staticmethod
    def generar(invernadero, plan):
        html = f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>Reporte - {invernadero.nombre} - {plan.nombre}</title>
<style> 
body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f7fa; }} 
table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }} 
th, td {{ border: 1px solid #333; padding: 8px; text-align: center; }} 
th {{ background-color: #2ecc71; color: white; }} 
h1, h2 {{ color: #2c3e50; }}
.card {{ background: white; padding: 20px; margin: 15px 0; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
.stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }}
.stat-box {{ background: #ecf0f1; padding: 15px; border-radius: 8px; text-align: center; }}
</style>
</head>
<body>
    <div class="card">
        <h1> Reporte de Riego Automatizado</h1>
        <h2>Invernadero: {invernadero.nombre}</h2>
        <h2>Plan: {plan.nombre}</h2>
    </div>
"""

       # reportes/html_reporte.py (parte corregida de la tabla de drones)
        # ================= TABLA DE DRONES ASIGNADOS =================
        html += """<div class="card">
        <h3>Asignación de Drones por Hilera</h3>
        <table>
            <tr><th>Hilera</th><th>Dron</th></tr>
        """
        # Ordenar por hilera para mejor presentación
        drones_por_hilera = {}
        actual_dron = invernadero.drones_asignados.primero
        while actual_dron is not None:
            dron = actual_dron.valor
            if dron.hilera_asignada not in drones_por_hilera:
                drones_por_hilera[dron.hilera_asignada] = []
            drones_por_hilera[dron.hilera_asignada].append(dron.nombre)
            actual_dron = actual_dron.siguiente

        # Mostrar en orden de hilera
        for hilera in sorted(drones_por_hilera.keys()):
            for dron_nombre in drones_por_hilera[hilera]:
                html += f"<tr><td>H{hilera}</td><td>{dron_nombre}</td></tr>\n"
        html += "</table></div>\n"

        # ================= ESTADÍSTICAS =================
        html += f"""
    <div class="card">
        <h3>Estadísticas del Proceso</h3>
        <div class="stats">
            <div class="stat-box">
                <h4>Tiempo Óptimo</h4>
                <p style="font-size: 24px; color: #2ecc71; margin: 10px 0;">{plan.tiempo_optimo} segundos</p>
            </div>
            <div class="stat-box">
                <h4>Agua Total</h4>
                <p style="font-size: 24px; color: #3498db; margin: 10px 0;">{plan.agua_total} litros</p>
            </div>
            <div class="stat-box">
                <h4>Fertilizante Total</h4>
                <p style="font-size: 24px; color: #e74c3c; margin: 10px 0;">{plan.fertilizante_total} gramos</p>
            </div>
        </div>
    </div>

    <div class="card">
        <h3>Eficiencia por Dron</h3>
        <table>
            <tr><th>Dron</th><th>Agua (L)</th><th>Fertilizante (g)</th></tr>
"""
        actual = plan.eficiencia_drones.primero
        while actual is not None:
            ef = actual.valor
            html += f"<tr><td>{ef.nombre}</td><td>{ef.agua}</td><td>{ef.fertilizante}</td></tr>\n"
            actual = actual.siguiente

        html += """</table></div>
    <div class="card">
        <h3>Instrucciones por Tiempo</h3>
        <table>
        <tr><th>Tiempo (s)</th>"""

        # Obtener nombres de drones para encabezados
        drones_nombres = []
        actual_dron = invernadero.drones_asignados.primero
        while actual_dron is not None:
            drones_nombres.append(actual_dron.valor.nombre)
            html += f"<th>{actual_dron.valor.nombre}</th>"
            actual_dron = actual_dron.siguiente
        html += "</tr>\n"

        # Instrucciones por tiempo
        tiempo_idx = 1
        actual_tiempo = plan.instrucciones_por_tiempo.primero
        while actual_tiempo is not None:
            instrucciones_lista = actual_tiempo.valor  # ListaSimple de InstruccionTiempo
            html += f"<tr><td>{tiempo_idx}</td>"
            
            # Para cada dron, buscar su instrucción en este tiempo
            for dron_nombre in drones_nombres:
                accion = "Esperar"  # Valor por defecto
                actual_inst = instrucciones_lista.primero
                while actual_inst is not None:
                    instruccion = actual_inst.valor
                    if instruccion.nombre_dron == dron_nombre:
                        accion = instruccion.accion
                        break
                    actual_inst = actual_inst.siguiente
                html += f"<td>{accion}</td>"
            
            html += "</tr>\n"
            tiempo_idx += 1
            actual_tiempo = actual_tiempo.siguiente

        html += """</table></div></body></html>"""

        os.makedirs("reportes/html", exist_ok=True)
        nombre_archivo = f"Reporte_{invernadero.nombre.replace(' ', '_')}_{plan.nombre.replace(' ', '_')}.html"
        ruta = f"reportes/html/{nombre_archivo}"
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(html)
        return ruta