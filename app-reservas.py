import datetime as dt
import numpy as np
import re
import uuid
import streamlit as st
from streamlit_option_menu import option_menu
from google_sheets import GoogleSheets
from google_calendar import GoogleCalendar
from send_email import send
import pytz

# Variables
page_title = "Club de Tenis"
page_icon = "🎾"
layout = "centered"

horas = ["9:00", "10:30", "12:00", "15:00", "17:00", "18:00", "19:30", "21:00"]
pistas = ["Pista 1", "Pista 2"]

document = "gestion-club-padel"
sheet = "reservas"
credentials = st.secrets["google"]["credential_google"]
id_calendar = st.secrets["id_calendar"]["id_calendar"]
time_zone = "America/Mexico_City"
local_tz = pytz.timezone('America/Mexico_City')

# Funciones
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def generate_uid():
    return str(uuid.uuid4())

def add_hour_and_half(time):
    parsed_time = dt.datetime.strptime(time, "%H:%M").time()
    new_time = (dt.datetime.combine(dt.date.today(), parsed_time) + dt.timedelta(hours=1, minutes=30)).time()
    return new_time.strftime("%H:%M")

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)

# Diseño de la página
st.image("assets/padel.jpeg")
st.markdown("<h1 style='text-align: center; color: #2E8B57;'>Club de Tenis</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555;'># Dirección del establecimiento #</p>", unsafe_allow_html=True)

selected = option_menu(
    menu_title=None,
    options=["Reservar", "Pistas", "Detalles"],
    icons=["calendar-date", "building", "clipboard-minus"],
    orientation="horizontal",
    styles={
        "container": {"padding": "5px", "background-color": "#fafafa"},
        "icon": {"color": "#2E8B57", "font-size": "25px"},
        "nav-link": {"font-size": "18px", "text-align": "center", "margin": "0px", "--hover-color": "#f0f0f0"},
        "nav-link-selected": {"background-color": "#2E8B57", "color": "white"},
    }
)

if selected == "Detalles":
    st.subheader("Ubicación")
    st.markdown("""<iframe src="https://www.google.com/maps/embed?pb=!1m14!1m12!1m3!1d1145.4788238030683!2d-99.17488306338723!3d19.51721351227803!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!5e0!3m2!1ses!2smx!4v1716911385713!5m2!1ses!2smx" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>""", unsafe_allow_html=True)

    st.subheader("Horarios")
    horarios = {
        "Lunes": "10:00 - 19:00",
        "Martes": "10:00 - 19:00",
        "Miércoles": "10:00 - 19:00",
        "Jueves": "10:00 - 19:00",
        "Viernes": "10:00 - 19:00",
        "Sábado": "10:00 - 15:00"
    }
    st.markdown("<div style='display: flex; justify-content: space-between; color: #444;'>"
                + "".join([f"<div><strong>{day}:</strong> {hours}</div>" for day, hours in horarios.items()])
                + "</div>", unsafe_allow_html=True)

    st.subheader("Contacto")
    st.markdown("<p style='color: #444;'>📞 5611922947</p>", unsafe_allow_html=True)

elif selected == "Pistas":
    st.image("assets/pista1.jpeg", width=600, caption="Esta es nuestra pista 1")
    st.image("assets/pista2.jpeg", width=600, caption="Esta es nuestra pista 2")

else:
    st.subheader("Reservar")
    with st.form(key='reservation_form'):
        c1, c2 = st.columns(2)

        nombre = c1.text_input("Tu nombre*")
        email = c2.text_input("Tu email*")
        fecha = c1.date_input("Fecha")

        if fecha:
            calendar = GoogleCalendar(credentials, id_calendar)
            hours_blocked = calendar.get_events_start_time(str(fecha))
            result_hours = np.setdiff1d(horas, hours_blocked)

        hora = c2.selectbox("Hora", result_hours)
        pista = c1.selectbox("Pista", pistas)
        notas = c2.text_area("Notas", placeholder="Opcional")

        enviar = st.form_submit_button("Reservar")

        if enviar:
            with st.spinner("Cargando ...."):
                if not nombre:
                    st.warning("El nombre es obligatorio")
                elif not email:
                    st.warning("El correo es obligatorio")
                elif not validate_email(email):
                    st.warning("El email no es válido")
                else:
                    hora_inicio = dt.datetime.strptime(hora, "%H:%M")
                    fecha_hora_inicio = dt.datetime.combine(fecha, hora_inicio.time())
                    fecha_hora_inicio = local_tz.localize(fecha_hora_inicio)  # Localiza la hora de inicio

                    fecha_hora_fin = fecha_hora_inicio + dt.timedelta(hours=1, minutes=30)  # Calcula la hora de fin

                    # Convertir a UTC para Google Calendar
                    start_time_utc = fecha_hora_inicio.astimezone(pytz.utc).isoformat()
                    end_time_utc = fecha_hora_fin.astimezone(pytz.utc).isoformat()

                    # Crear el evento en Google Calendar
                    calendar.create_event(nombre, start_time_utc, end_time_utc, time_zone)

                    # Crear un registro en Google Sheets
                    uid = generate_uid()
                    data = [[nombre, email, pista, str(fecha), hora, notas, uid]]
                    gs = GoogleSheets(credentials, document, sheet)
                    range = gs.get_last_row_range()
                    gs.write_data(range, data)

                    # Enviar correo de confirmación
                    send(email, nombre, fecha, hora, pista)
                    st.success("Su pista ha sido reservada exitosamente.")
