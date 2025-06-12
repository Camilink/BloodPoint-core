# bloodpoint_app/utils/excel_templates.py

from openpyxl import Workbook
from bloodpoint_app.models import campana

def generar_excel_campana(campana_id, response):
    campana_obj = campana.objects.get(id_campana=campana_id)

    wb = Workbook()
    ws = wb.active
    ws.title = "Resumen Campaña"

    ws.append([
        "ID Campaña",
        "Nombre Campaña",
        "Fecha Inicio",
        "Fecha Término",
        "Meta Donaciones (unidades)",
        "Donaciones Realizadas (unidades)",
        "Porcentaje Cumplimiento (%)",
        "Total ML Donados",
        "Donantes Únicos",
        "Estado Campaña",
        "Representante Responsable",
        "Centro de Donación",
    ])

    total_donaciones = campana_obj.donacion_set.count()
    total_ml = sum(d.ml_donados for d in campana_obj.donacion_set.all())
    porcentaje = (total_donaciones / campana_obj.meta) * 100 if campana_obj.meta else 0
    donantes_unicos = campana_obj.donacion_set.values('donante').distinct().count()

    ws.append([
        campana_obj.id,
        campana_obj.nombre,
        campana_obj.fecha_inicio.strftime('%Y-%m-%d'),
        campana_obj.fecha_termino.strftime('%Y-%m-%d'),
        campana_obj.meta,
        total_donaciones,
        f"{porcentaje:.1f}%",
        total_ml,
        donantes_unicos,
        campana_obj.estado,
        str(campana_obj.representante_responsable),
        str(campana_obj.centro_donacion),
    ])

    wb.save(response)
