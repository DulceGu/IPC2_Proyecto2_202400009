# app.py
import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from modelos.sistema import SistemaRiego
from controladores.xml_handler import XMLHandler
from controladores.simulador import Simulador
from reportes.html_reporte import HTMLReporte
from reportes.dot_reporte import DOTReporte

app = Flask(__name__)
app.secret_key = "ipc2_proyecto2_2024"

sistema = SistemaRiego()
simulador = Simulador(sistema)

# app.py (solo la parte de get_system_stats)
def get_system_stats():
    total_drones = 0
    total_invernaderos = 0
    total_planes = 0
    invernaderos_data = []

    print("\n=== DEPURACIÓN: get_system_stats ===")

    # Contar drones en sistema
    actual_dron = sistema.lista_drones.primero
    print("Drones en sistema:")
    while actual_dron is not None:
        total_drones += 1
        dron = actual_dron.valor
        print(f"  - {dron.nombre} (ID:{dron.id}) -> Hilera: {dron.hilera_asignada}")
        actual_dron = actual_dron.siguiente

    # Procesar invernaderos
    actual_inv = sistema.lista_invernaderos.primero
    print("Invernaderos en sistema:")
    while actual_inv is not None:
        total_invernaderos += 1
        inv = actual_inv.valor
        print(f"  - {inv.nombre}:")
        
        # Contar planes por invernadero
        planes_count = 0
        actual_plan = inv.planes_riego.primero
        while actual_plan is not None:
            planes_count += 1
            total_planes += 1
            actual_plan = actual_plan.siguiente

        # Obtener drones del invernadero
        drones_inv = []
        actual_dron_inv = inv.drones_asignados.primero
        print(f"    Drones asignados a {inv.nombre}:")
        while actual_dron_inv is not None:
            dron = actual_dron_inv.valor
            print(f"      - {dron.nombre} -> Hilera {dron.hilera_asignada}")
            drones_inv.append({
                'nombre': dron.nombre,
                'hilera_asignada': dron.hilera_asignada
            })
            actual_dron_inv = actual_dron_inv.siguiente

        invernaderos_data.append({
            'nombre': inv.nombre,
            'numero_hileras': inv.numero_hileras,
            'plantas_por_hilera': inv.plantas_por_hilera,
            'total_planes': planes_count,
            'drones': drones_inv
        })
        actual_inv = actual_inv.siguiente

    print(f"=== RESUMEN: {total_drones} drones, {total_invernaderos} invernaderos, {total_planes} planes ===\n")
    return total_drones, total_invernaderos, total_planes, invernaderos_data

@app.route('/')
def index():
    total_drones, total_invernaderos, total_planes, invernaderos = get_system_stats()
    return render_template('index.html', 
                         total_drones=total_drones,
                         total_invernaderos=total_invernaderos,
                         total_planes=total_planes,
                         invernaderos=invernaderos)

@app.route('/cargar', methods=['GET', 'POST'])
def cargar():
    if request.method == 'POST':
        archivo = request.files.get('archivo')
        if not archivo or archivo.filename == '':
            flash("No se seleccionó archivo.", "error")
        elif not archivo.filename.lower().endswith('.xml'):
            flash("Archivo inválido. Debe ser .xml", "error")
        else:
            ruta = os.path.join('uploads', archivo.filename)
            os.makedirs('uploads', exist_ok=True)
            archivo.save(ruta)
            try:
                XMLHandler.cargar_configuracion(ruta, sistema)
                flash("Configuración cargada exitosamente.", "success")
            except Exception as e:
                flash(f"Error al cargar: {str(e)}", "error")
    return render_template('cargar.html')

@app.route('/simular', methods=['GET', 'POST'])
def simular():
    if request.method == 'POST':
        inv_nombre = request.form.get('invernadero')
        plan_nombre = request.form.get('plan')
        if not inv_nombre or not plan_nombre:
            flash("Debe seleccionar invernadero y plan.", "error")
            return redirect(url_for('simular'))

        exito = simulador.simular_plan(inv_nombre, plan_nombre)
        if exito:
            inv = sistema.buscar_invernadero_por_nombre(inv_nombre)
            plan = inv.buscar_plan_por_nombre(plan_nombre)
            if plan:
                ruta_html = HTMLReporte.generar(inv, plan)
                return send_file(ruta_html, as_attachment=False)
            else:
                flash("Plan no encontrado.", "error")
        else:
            flash("Error al simular el plan. Revisa la configuración y nombres.", "error")
    
    # Obtener lista de invernaderos para el select
    invernaderos = []
    actual = sistema.lista_invernaderos.primero
    while actual:
        invernaderos.append(actual.valor.nombre)
        actual = actual.siguiente
    
    return render_template('simular.html', invernaderos=invernaderos)

@app.route('/graficar/<invernadero>/<plan>/<int:tiempo>')
def graficar(invernadero, plan, tiempo):
    inv = sistema.buscar_invernadero_por_nombre(invernadero)
    if not inv:
        flash("Invernadero no encontrado.", "error")
        return redirect(url_for('index'))
    
    plan_obj = inv.buscar_plan_por_nombre(plan)
    if not plan_obj:
        flash("Plan no encontrado.", "error")
        return redirect(url_for('index'))

    try:
        ruta_svg = DOTReporte.generar_tda(plan_obj, tiempo)
        return send_file(ruta_svg, mimetype='image/svg+xml')
    except Exception as e:
        flash(f"Error al generar gráfico: {str(e)}", "error")
        return redirect(url_for('index'))

@app.route('/salida')
def salida():
    ruta = "reportes/salida.xml"
    try:
        # Asegurarnos de que el directorio existe
        os.makedirs("reportes", exist_ok=True)
        
        # Generar el archivo de salida
        from controladores.xml_handler import XMLHandler
        XMLHandler.generar_salida(ruta, sistema)
        
        # Enviar el archivo como descarga
        return send_file(ruta, as_attachment=True, download_name="salida.xml")
    except Exception as e:
        flash(f"Error al generar salida: {str(e)}", "error")
        return redirect(url_for('index'))

@app.route('/ayuda')
def ayuda():
    return render_template('ayuda.html')

if __name__ == '__main__':
    # Crear directorios necesarios
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('reportes', exist_ok=True)
    os.makedirs('reportes/html', exist_ok=True)
    os.makedirs('reportes/dot', exist_ok=True)
    
    app.run(debug=True)