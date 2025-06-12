from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from bloodpoint_app.models import campana, TIPO_SANGRE_CHOICES

def generar_excel_campana(campana_id, response):
    campana_obj = campana.objects.get(id_campana=campana_id)

    wb = Workbook()
    ws = wb.active
    ws.title = "Resumen Campaña"

    # Estilos
    title_font = Font(size=16, bold=True)
    subtitle_font = Font(size=12, italic=True)
    bold_font = Font(bold=True)
    gray_font = Font(size=9, italic=True, color="888888")
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill("solid", fgColor="FF0000")
    center_alignment = Alignment(horizontal="center", vertical="center")
    thin_border = Border(
        left=Side(style='thin'), right=Side(style='thin'),
        top=Side(style='thin'), bottom=Side(style='thin')
    )

    # --- TÍTULO Y DESCRIPCIÓN ---
    ws.merge_cells('A1:J1')
    ws['A1'] = campana_obj.nombre_campana
    ws['A1'].font = title_font
    ws['A1'].alignment = center_alignment

    nombre_representante = campana_obj.id_representante.full_name()
    ws.merge_cells('A2:J2')
    ws['A2'] = f"Representante: {nombre_representante}"
    ws['A2'].font = bold_font
    ws['A2'].alignment = center_alignment

    fecha_inicio = campana_obj.fecha_campana.strftime('%Y-%m-%d')
    fecha_termino = campana_obj.fecha_termino.strftime('%Y-%m-%d') if campana_obj.fecha_termino else "N/A"
    ws.merge_cells('A3:J3')
    ws['A3'] = f"Desde {fecha_inicio} hasta {fecha_termino}"
    ws['A3'].font = subtitle_font
    ws['A3'].alignment = center_alignment

    # --- DATOS DE CAMPAÑA ---
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

    ws.append([])  # Fila vacía (fila 4)
    ws.append(headers)  # Fila 5

    for col_num, _ in enumerate(headers, 1):
        cell = ws.cell(row=5, column=col_num)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_alignment
        cell.border = thin_border

    total_donaciones = campana_obj.donacion_set.count()
    total_ml = sum(d.cantidad_donacion for d in campana_obj.donacion_set.all())
    meta = int(campana_obj.meta) if campana_obj.meta else 0
    porcentaje = (total_donaciones / meta) * 100 if meta else 0

    ws.append([
        campana_obj.id_campana,
        campana_obj.nombre_campana,
        fecha_inicio,
        fecha_termino,
        campana_obj.meta,
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

    # --- LEYENDA FINAL ---
    ws.merge_cells('A8:J8')
    ws['A8'] = "Datos generados automáticamente por BloodPoint"
    ws['A8'].font = gray_font
    ws['A8'].alignment = center_alignment

    # --- SEGUNDA HOJA: ML por tipo de sangre ---
    ws2 = wb.create_sheet(title="ML por Tipo de Sangre")
    sub_headers = ["Tipo de Sangre", "Total ML Donados"]
    ws2.append(sub_headers)

    for col_num, header in enumerate(sub_headers, 1):
        cell = ws2.cell(row=1, column=col_num)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_alignment
        cell.border = thin_border

    for row_num, (tipo, _) in enumerate(TIPO_SANGRE_CHOICES, 2):
        total_ml_tipo = sum(
            d.cantidad_donacion
            for d in campana_obj.donacion_set.filter(id_donante__tipo_sangre=tipo)
        )
        ws2.append([tipo, total_ml_tipo])
        for col_num in range(1, 3):
            cell = ws2.cell(row=row_num, column=col_num)
            cell.alignment = center_alignment
            cell.border = thin_border

    # --- AJUSTE DE ANCHOS ---
    for sheet in [ws, ws2]:
        for col in sheet.columns:
            max_length = max(len(str(cell.value)) if cell.value else 0 for cell in col)
            col_letter = col[0].column_letter
            sheet.column_dimensions[col_letter].width = max_length + 2

    # --- GUARDAR ---
    wb.save(response)
