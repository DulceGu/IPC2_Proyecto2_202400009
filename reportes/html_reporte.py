# reportes/html_reporte.py
import os

class HTMLReporte:
    @staticmethod
    def generar(invernadero, plan):
        html = f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>Reporte - {invernadero.nombre} - {plan.nombre}</title>
<style> body {{ font-family: Arial, sans-serif; margin: 20px; }} table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }} th, td {{ border: 1px solid #333; padding: 8px; text-align: center; }} th {{ background-color: #f2f2f2; }} h1, h2 {{ color: #2c3e50; }} </style>
</head><body>
    <h1>Reporte de Riego</h1>
    <h2>Invernadero: {invernadero.nombre}</h2>
    <h2>Plan: {plan.nombre}</h2>
    <h3>Estadísticas</h3>
    <p><strong>Tiempo óptimo:</strong> {plan.tiempo_optimo} segundos</p>
    <p><strong>Agua total:</strong> {plan.agua_total} litros</p>
    <p><strong>Fertilizante total:</strong> {plan.fertilizante_total} gramos</p>
    <h3>Eficiencia por dron</h3>
    <table>
        <tr><th>Dron</th><th>Agua (L)</th><th>Fertilizante (g)</th></tr>
"""
        # eficiencia_drones (ListaSimple)
        actual = plan.eficiencia_drones.primero
        while actual is not None:
            ef = actual.valor
            html += f"<tr><td>{ef.nombre}</td><td>{ef.agua}</td><td>{ef.fertilizante}</td></tr>\n"
            actual = actual.siguiente

        html += "</table>\n<h3>Instrucciones por tiempo</h3>\n<table>\n<tr><th>Tiempo (s)</th>"

        # encabezado con nombres de drones (si hay alguna instrucción)
        drones_nombres = []
        if plan.instrucciones_por_tiempo.tamanio > 0 and plan.instrucciones_por_tiempo.primero is not None:
            primer_tiempo = plan.instrucciones_por_tiempo.primero.valor
            for dron_nombre in primer_tiempo.keys():
                drones_nombres.append(dron_nombre)
                html += f"<th>{dron_nombre}</th>"
        html += "</tr>\n"

        tiempo_idx = 1
        actual_tiempo = plan.instrucciones_por_tiempo.primero
        while actual_tiempo is not None:
            instrucciones = actual_tiempo.valor
            html += f"<tr><td>{tiempo_idx}</td>"
            for dron in drones_nombres:
                accion = instrucciones.get(dron, "Esperar")
                html += f"<td>{accion}</td>"
            html += "</tr>\n"
            tiempo_idx += 1
            actual_tiempo = actual_tiempo.siguiente

        html += "</table></body></html>"

        os.makedirs("reportes/html", exist_ok=True)
        ruta = f"reportes/html/Reporte_{invernadero.nombre}_{plan.nombre}.html"
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(html)
        return ruta

from estructuras.lista_simple import ListaSimple