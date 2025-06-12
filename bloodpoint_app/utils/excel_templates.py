# bloodpoint_app/utils/excel_templates.py

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from bloodpoint_app.models import campana

def generar_excel_campana(campana_id, response):
    campana_obj = campana.objects.get(id_campana=campana_id)

    wb = Workbook()
    ws = wb.active
    ws.title = "Resumen Campaña"

    # Estilos
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="C0392B", end_color="C0392B", fill_type="solid")
    center_alignment = Alignment(horizontal="center", vertical="center")
    thin_border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )

    headers = [
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
    ]
    ws.append(headers)

    # Aplicar estilos al encabezado
    for col_num, cell in enumerate(ws[1], 1):
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_alignment
        cell.border = thin_border

    # Cálculos
    total_donaciones = campana_obj.donacion_set.count()
    total_unidades_donadas = sum(d.cantidad_donacion for d in campana_obj.donacion_set.all())
    donantes_unicos = campana_obj.donacion_set.values('id_donante').distinct().count()

    meta = int(campana_obj.meta) if campana_obj.meta else 0
    porcentaje = (total_donaciones / meta) * 100 if meta else 0

    representante = (
        campana_obj.id_representante.full_name()
        if campana_obj.id_representante else "No asignado"
    )

    data_row = [
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
    ]
    ws.append(data_row)

    # Estilo para fila de datos
    for row in ws.iter_rows(min_row=2, max_row=2):
        for cell in row:
            cell.alignment = center_alignment
            cell.border = thin_border

    # Ajustar anchos de columna automáticamente
    for col in ws.columns:
        max_length = 0
        col_letter = col[0].column_letter
        for cell in col:
            if cell.value:
                max_length = max(max_length, len(str(cell.value)))
        ws.column_dimensions[col_letter].width = max_length + 2

    # Guardar
    wb.save(response)
