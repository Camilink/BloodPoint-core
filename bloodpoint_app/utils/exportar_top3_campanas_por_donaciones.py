from openpyxl import Workbook
from datetime import datetime
from io import BytesIO
from bloodpoint_app.models import campana, donacion

def exportar_top3_campanas_por_donaciones():
    campañas_data = []

    for c in campana.objects.all():
        donaciones = donacion.objects.filter(campana_relacionada=c)
        total_donaciones = donaciones.count()
        total_validadas = donaciones.filter(validada=True).count()
        total_intencionadas = donaciones.filter(es_intencion=True).count()
        total_sangre = sum([d.cantidad_donacion for d in donaciones])
        nuevos_donantes = sum([1 for d in donaciones if d.id_donante.nuevo_donante])

        porcentaje_nuevos = (nuevos_donantes / total_donaciones * 100) if total_donaciones else 0

        # Convertir meta a número
        try:
            meta_valor = float(c.meta) if c.meta else 0
        except (ValueError, TypeError):
            meta_valor = 0

        porcentaje_meta = (total_sangre / meta_valor * 100) if meta_valor else 0

        campañas_data.append({
            "campana": c,
            "total_donaciones": total_donaciones,
            "validadas": total_validadas,
            "intencionadas": total_intencionadas,
            "total_sangre": total_sangre,
            "meta": meta_valor,
            "porc_meta": porcentaje_meta,
            "porc_nuevos": porcentaje_nuevos
        })

    # Ordenar por total de donaciones
    top3 = sorted(campañas_data, key=lambda x: x["total_donaciones"], reverse=True)[:3]

    # Crear Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Top 3 campañas"

    headers = [
        "ID campaña", "Nombre", "Fecha inicio", "Fecha fin", "Comuna", "Centro",
        "Representante", "Meta (ml)", "Recolectado (ml)", "% meta",
        "Donaciones", "Validadas", "Intencionadas", "% nuevos donantes"
    ]
    ws.append(headers)

    for data in top3:
        c = data["campana"]
        ws.append([
            c.id_campana,
            c.nombre_campana,
            c.fecha_campana,
            c.fecha_termino,
            c.id_centro.comuna if c.id_centro else "",
            c.id_centro.nombre_centro if c.id_centro else "",
            f"{c.id_representante.nombre} {c.id_representante.apellido}" if c.id_representante else "",
            data["meta"],
            data["total_sangre"],
            round(data["porc_meta"], 2),
            data["total_donaciones"],
            data["validadas"],
            data["intencionadas"],
            round(data["porc_nuevos"], 2)
        ])

    # Guardar en memoria y devolver como bytes
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    return output.getvalue()
