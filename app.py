import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from modelos.sistema import SistemaRiego
from controladores.xml_handler import XMLHandler
from controladores.simulador import Simulador
from reportes.html_reporte import HTMLReporte
from flask import send_file


app = Flask(__name__)
app.secret_key = "ipc2_proyecto2"

sistema = SistemaRiego()
simulador = Simulador(sistema)

@app.route('/')
def index():
    return render_template('index.html')

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
    # listar invernaderos para el select
    invernaderos = []
    actual = sistema.lista_invernaderos.primero
    while actual:
        invernaderos.append(actual.valor.nombre)
        actual = actual.siguiente
    return render_template('simular.html', invernaderos=invernaderos)

@app.route('/ayuda')
def ayuda():
    return render_template('ayuda.html')

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/salida')
def salida():
    ruta = "reportes/salida.xml"
    try:
        from controladores.xml_handler import XMLHandler
        XMLHandler.generar_salida(ruta, sistema)
        return send_file(ruta, as_attachment=True)
    except Exception as e:
        flash(f"Error al generar salida: {str(e)}", "error")
        return redirect(url_for('index'))
