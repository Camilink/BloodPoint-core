from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage
from django.utils import timezone
from io import BytesIO
from bloodpoint_app.models import campana, donacion
from bloodpoint_app.views import generar_excel_campana
import os


class Command(BaseCommand):
    help = 'Envía alertas de stock de sangre por campaña en curso a sus representantes'

    def handle(self, *args, **kwargs):
        hoy = timezone.now().date()

        campañas_en_curso = campana.objects.filter(
            fecha_campana__lte=hoy,
            fecha_termino__gte=hoy
        )

        for campaña in campañas_en_curso:
            representante = campaña.id_representante
            if not representante or not representante.user or not representante.user.email:
                self.stdout.write(f"No se encontró email para el representante de la campaña '{campaña.nombre_campana}'")
                continue

            email_destino = representante.user.email

            cuerpo = (
                f"Estimado/a {representante.full_name()},\n\n"
                f"Adjunto encontrará el reporte actualizado de stock para la campaña \"{campaña.nombre_campana}\".\n\n"
                f"Gracias por su labor.\n\nEquipo BloodPoint"
            )

            # Generar el Excel
            excel_buffer = BytesIO()
            generar_excel_campana(campaña.id_campana, excel_buffer)

            # Crear el correo con adjunto
            email = EmailMessage(
                subject=f"[BloodPoint] Reporte de stock campaña: {campaña.nombre_campana}",
                body=cuerpo,
                from_email=os.environ.get("GMAIL_EMAIL"),
                to=[email_destino],
            )
            email.attach(
                f"reporte_campaña_{campaña.id_campana}.xlsx",
                excel_buffer.getvalue(),
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            email.send()

            self.stdout.write(f"Correo con Excel enviado a {email_destino} para campaña '{campaña.nombre_campana}'")
