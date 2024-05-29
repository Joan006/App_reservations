import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st


def send_email(email, nombre, fecha, hora, pista, nota, sender_email):
    # Credenciales
    user = st.secrets["smtp_user"]
    password = st.secrets["smtp_password"]
    # config. Servidor
    msg = MIMEMultipart()

    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Parametros del mensaje
    msg["From"] = sender_email
    msg["To"] = email
    msg["Subject"] = "Reserva de Pista"

    message = f"""
    Hola{nombre},
    Su reserva , ha ssido realizada con exito,
    Fecha: {fecha}
    Hora: {hora}
    pista: {pista}

    Gracias por confiar en nosotros.
    Saludos
    """
    msg.attach(MIMEText(message, "plain"))

    # conexion al servidor

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
