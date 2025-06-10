import csv
from io import StringIO
from django.db.models import Count, Sum, Q
from django.db.models.functions import Cast
from django.db.models import IntegerField
from tu_app.models import campana

def generar_csv_resumen_campana(campana_id):
    campaña = campana.objects.annotate(
        total_donaciones=Count('donacion', filter=Q(donacion__tipo_donacion='campana')),
        total_ml=Sum('donacion__cantidad_donacion', filter=Q(donacion__tipo_donacion='campana')),
        donantes_unicos=Count('donacion__id_donante', distinct=True, filter=Q(donacion__tipo_donacion='campana')),
        meta_int=Cast('meta', IntegerField())
    ).select_related('id_representante', 'id_centro').get(id_campana=campana_id)

    output = StringIO()
    writer = csv.writer(output)

    writer.writerow([
        'ID Campaña',
        'Nombre Campaña',
        'Fecha Inicio',
        'Fecha Término',
        'Meta Donaciones (unidades)',
        'Donaciones Realizadas (unidades)',
        'Porcentaje Cumplimiento (%)',
        'Total ML Donados',
        'Donantes Únicos',
        'Estado Campaña',
        'Representante Responsable',
        'Centro de Donación',
    ])

    meta = campaña.meta_int or 0
    total = campaña.total_donaciones or 0
    porcentaje = round(100 * total / meta, 1) if meta > 0 else None

    representante = ''
    if campaña.id_representante:
        representante = f'{campaña.id_representante.nombre} {campaña.id_representante.apellido}'

    centro = campaña.id_centro.nombre_centro if campaña.id_centro else ''

    writer.writerow([
        campaña.id_campana,
        campaña.nombre_campana,
        campaña.fecha_campana,
        campaña.fecha_termino,
        meta,
        total,
        f'{porcentaje}%' if porcentaje is not None else '',
        campaña.total_ml or 0,
        campaña.donantes_unicos or 0,
        campaña.estado,
        representante,
        centro,
    ])

    output.seek(0)
    return output.getvalue()
