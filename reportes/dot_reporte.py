# reportes/dot_reporte.py
import os

class DOTReporte:
    @staticmethod
    def generar_tda(invernadero, plan, tiempo_t):
        codigo_dot = 'digraph ColaRiegos {\\n    rankdir=LR;\\n    node [shape=record, height=0.1];\\n'
        actual = plan.orden_riego.primero
        contador = 1
        while actual is not None:
            hilera, pos = actual.valor
            codigo_dot += f'    nodo{contador} [label="{{<f0> H{hilera}-P{pos} | <f1> }}"];\n'
            contador += 1
            actual = actual.siguiente

        # Poner flechas
        for i in range(1, contador):
            if i + 1 < contador:
                codigo_dot += f'    nodo{i}:f1 -> nodo{i + 1}:f0;\n'

        codigo_dot += '}'

        os.makedirs("reportes/dot", exist_ok=True)
        ruta_dot = f"reportes/dot/estado_t{tiempo_t}.dot"
        with open(ruta_dot, "w", encoding="utf-8") as f:
            f.write(codigo_dot)

        os.makedirs("reportes/html", exist_ok=True)
        ruta_svg = f"reportes/html/estado_t{tiempo_t}.svg"
        # Ejecuta dot si está disponible en el sistema
        os.system(f'dot -Tsvg "{ruta_dot}" -o "{ruta_svg}"')
        return ruta_svg


