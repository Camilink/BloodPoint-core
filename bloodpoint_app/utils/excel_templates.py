# bloodpoint_app/utils/excel_templates.py

from openpyxl import Workbook
from bloodpoint_app.models import campana

def generar_excel_campana(campana_id, response):
    campana_obj = campana.objects.get(id_campana=campana_id)

    wb = Workbook()
    ws = wb.active
    ws.title = "Resumen Campaña"

    # Encabezado
    ws.append([
        "ID Campaña",
        "Nombre Campaña",
        "Fecha Inicio",
        "Fecha Término",
        "Meta Donaciones (unidades)",
        "Donaciones Realizadas (unidades)",
        "Porcentaje Cumplimiento (%)",
        "Total Unidades Donadas",
        "Donantes Únicos",
        "Estado Campaña",
        "Representante Responsable",
    ])

    # Datos agregados
    total_donaciones = campana_obj.donacion_set.count()
    total_unidades_donadas = sum(d.cantidad_donacion for d in campana_obj.donacion_set.all())
    donantes_unicos = campana_obj.donacion_set.values('id_donante').distinct().count()

    meta = int(campana_obj.meta) if campana_obj.meta else 0
    porcentaje = (total_donaciones / meta) * 100 if meta else 0

    representante = (
        campana_obj.id_representante.full_name()
        if campana_obj.id_representante else "No asignado"
    )

    ws.append([
        campana_obj.id_campana,
        campana_obj.nombre_campana,
        campana_obj.fecha_campana.strftime('%Y-%m-%d'),
        campana_obj.fecha_termino.strftime('%Y-%m-%d'),
        meta,
        total_donaciones,
        f"{porcentaje:.1f}%",
        total_unidades_donadas,
        donantes_unicos,
        campana_obj.estado,
        representante,
    ])

    wb.save(response)
