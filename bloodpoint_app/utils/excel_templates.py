from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from bloodpoint_app.models import campana, TIPO_SANGRE_CHOICES

def generar_excel_campana(campana_id, response):
    campana_obj = campana.objects.get(id_campana=campana_id)

    wb = Workbook()
    ws = wb.active
    ws.title = "Resumen Campaña"

    # Estilos
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill("solid", fgColor="FF0000")
    center_alignment = Alignment(horizontal="center", vertical="center")
    left_alignment = Alignment(horizontal="left", vertical="center")
    bold_font = Font(bold=True)
    title_font = Font(size=16, bold=True, color="9C0006")
    subtitle_font = Font(size=12, bold=True)
    thin_border = Border(
        left=Side(style='thin'), right=Side(style='thin'),
        top=Side(style='thin'), bottom=Side(style='thin')
    )

    # Datos para los cálculos
    total_donaciones = campana_obj.donacion_set.count()
    total_ml = sum(d.cantidad_donacion for d in campana_obj.donacion_set.all())
    meta = int(campana_obj.meta) if campana_obj.meta else 0
    porcentaje = (total_donaciones / meta) * 100 if meta else 0
    nombre_representante = campana_obj.id_representante.full_name()
    fecha_inicio = campana_obj.fecha_campana.strftime('%Y-%m-%d')
    fecha_termino = campana_obj.fecha_termino.strftime('%Y-%m-%d') if campana_obj.fecha_termino else "N/A"

    # Título principal
    ws.merge_cells('A1:J1')
    cell = ws['A1']
    cell.value = f"Resumen de la Campaña: {campana_obj.nombre_campana}"
    cell.font = title_font
    cell.alignment = center_alignment

    # Representante
    ws.merge_cells('A2:J2')
    cell = ws['A2']
    cell.value = f"Representante: {nombre_representante}"
    cell.font = subtitle_font
    cell.alignment = center_alignment

    # Fechas
    ws.merge_cells('A3:J3')
    cell = ws['A3']
    cell.value = f"Fecha de inicio: {fecha_inicio} | Fecha de término: {fecha_termino}"
    cell.font = subtitle_font
    cell.alignment = center_alignment

    # Espacio visual
    ws.append([])

    # Encabezados de tabla
    headers = [
        "ID Campaña",
        "Nombre Campaña",
        "Fecha Inicio",
        "Fecha Término",
        "Meta Donaciones (unidades)",
        "Donaciones Realizadas (unidades)",
        "Porcentaje Cumplimiento (%)",
        "Total ML Donados",
        "Estado Campaña",
        "Representante Responsable",
    ]
    ws.append(headers)
    for col_num, _ in enumerate(headers, 1):
        cell = ws.cell(row=5, column=col_num)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_alignment
        cell.border = thin_border

    # Datos de la campaña
    ws.append([
        campana_obj.id_campana,
        campana_obj.nombre_campana,
        fecha_inicio,
        fecha_termino,
        meta,
        total_donaciones,
        f"{porcentaje:.1f}%",
        total_ml,
        campana_obj.estado,
        nombre_representante,
    ])
    for col_num in range(1, len(headers) + 1):
        cell = ws.cell(row=6, column=col_num)
        cell.alignment = center_alignment
        cell.border = thin_border

    # Segunda hoja: Total ML por tipo de sangre
    ws2 = wb.create_sheet(title="ML por Tipo de Sangre")
    sub_headers = ["Tipo de Sangre", "Total ML Donados"]
    ws2.append(sub_headers)
    for col_num, header in enumerate(sub_headers, 1):
        cell = ws2.cell(row=1, column=col_num)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_alignment
        cell.border = thin_border

    for row_num, (tipo, _) in enumerate(TIPO_SANGRE_CHOICES, start=2):
        total_ml_tipo = sum(
            d.cantidad_donacion
            for d in campana_obj.donacion_set.filter(id_donante__tipo_sangre=tipo)
        )
        ws2.append([tipo, total_ml_tipo])
        for col_num in range(1, 3):
            cell = ws2.cell(row=row_num, column=col_num)
            cell.alignment = center_alignment
            cell.border = thin_border

    # Ajustar anchos sin usar MergedCell (evita error)
    for sheet in [ws, ws2]:
        for col_cells in sheet.columns:
            normal_cells = [cell for cell in col_cells if not isinstance(cell, type(sheet.cell(row=1, column=1)._parent.cell(1,1)))]
            if not normal_cells:
                continue
            max_length = max(len(str(cell.value)) if cell.value else 0 for cell in normal_cells)
            col_letter = normal_cells[0].column_letter
            sheet.column_dimensions[col_letter].width = max_length + 2

    # Guardar
    wb.save(response)
