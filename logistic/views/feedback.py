import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.shortcuts import render
from django.core.mail import send_mail


def send_email_to_client(request):
    if request.method == 'POST':
        cliente_email = request.POST.get('cliente_email')
        # Reemplaza esto con la URL real de tu formulario Google
        formulario_google_url = 'https://forms.gle/MzHw5qdFXaML5nqz5'

        mensaje = f"""
        Hola!,

        Gracias por utilizar nuestro servicio de apoyo logístico para tu evento. Nos encantaría recibir tus comentarios sobre cómo fue tu experiencia. Por favor, completa este formulario de calificación: {formulario_google_url}

        ¡Esperamos verte de nuevo pronto!

        Saludos,
        Equipo de apoyo logístico CCSA.
        """

        # Enviar el correo electrónico
        send_mail(
            'Calificación de servicio de apoyo logístico',  # Asunto del correo
            mensaje,  # Cuerpo del correo
            'apoyologisticoccsa@gmail.com',  # Correo electrónico remitente
            [cliente_email],  # Lista de destinatarios
            fail_silently=False,
        )
        msj_exito = "Correo enviado con éxito al cliente"
        # Renderizar una página de éxito después de enviar el correo
        return render(request, 'feedback.html', {"msj_exito": msj_exito})

    # Renderizar el formulario para capturar el correo del cliente
    return render(request, 'feedback.html')
