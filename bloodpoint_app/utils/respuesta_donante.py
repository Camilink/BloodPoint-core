from django.core.mail import EmailMessage
from bloodpoint_app.models import respuestas_representante
from django.utils import timezone
import os

def enviar_respuesta_a_donante(id_respuesta):
    try:
        respuesta = respuestas_representante.objects.select_related('id_pregunta__user', 'id_representante').get(id=id_respuesta)
        pregunta = respuesta.id_pregunta
        donante_user = pregunta.user
        representante = respuesta.id_representante

        email_destino = donante_user.email
        if not email_destino:
            return

        cuerpo = (
            f"Hola,\n\n"
            f"Hemos recibido una respuesta a tu pregunta enviada el {pregunta.fecha_pregunta.strftime('%d-%m-%Y %H:%M')}:\n\n"
            f"Pregunta: \"{pregunta.pregunta}\"\n\n"
            f"Respuesta del representante ({representante.full_name()}) "
            f"enviada el {respuesta.fecha_respuesta.strftime('%d-%m-%Y %H:%M')}:\n"
            f"\"{respuesta.respuesta}\"\n\n"
            f"Gracias por contactarte con nosotros.\n\n"
            f"Equipo BloodPoint"
        )

        email = EmailMessage(
            subject=f"[BloodPoint] Respuesta a tu consulta",
            body=cuerpo,
            from_email=os.environ.get("GMAIL_EMAIL"),
            to=[email_destino],
        )
        email.send()

    except respuestas_representante.DoesNotExist:
        pass
