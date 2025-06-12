# bloodpoint_app/utils/excel_templates.py

from openpyxl import Workbook
from ..models import Campana  # ajusta si la estructura es diferente

def generar_excel_campana(campana_id, response):
    campana = Campana.objects.get(id=campana_id)

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

    total_donaciones = campana.donacion_set.count()
    total_ml = sum(d.ml_donados for d in campana.donacion_set.all())
    porcentaje = (total_donaciones / campana.meta_donaciones) * 100 if campana.meta_donaciones else 0
    donantes_unicos = campana.donacion_set.values('donante').distinct().count()

    ws.append([
        campana.id,
        campana.nombre,
        campana.fecha_inicio.strftime('%Y-%m-%d'),
        campana.fecha_termino.strftime('%Y-%m-%d'),
        campana.meta_donaciones,
        total_donaciones,
        f"{porcentaje:.1f}%",
        total_ml,
        donantes_unicos,
        campana.estado,
        str(campana.representante_responsable),
        str(campana.centro_donacion),
    ])

    wb.save(response)
