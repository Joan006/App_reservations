import streamlit as st
from streamlit_option_menu import option_menu
from send_email import send
from google_sheets import GoogleSheets
import re
import uuid

# Variables
page_title = "Club de padel"
page_icon = "🎾"
layout = "centered"

horas = ["9:00", "10:30", "12:00", "15:00", "17:00", "18:00", "19:30", "21:00"]
pistas = ["Pista 1", "Pista2"]

document = "gestion-club-padel"
sheet = "reservas"
credentials = st.secrets["google"]["credential_google"]

# Funciones
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    # Usa re.match para verificar si el email coincide con el patrón
    if re.match(pattern, email):
        return True
    else:
        return False

def generate_uid():
    return str(uuid.uuid4())

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)


# Diseño de la pagina
st.image("assets/padel.jpeg")
st.title("Club de padel")
st.text("# Direccion del establecimiento #")

selected = option_menu(menu_title=None, options=["Reservar", "Pistas", "Detalles"], icons=["calendar-date", "building", "clipboard-minus"], orientation="horizontal")


if selected == "Detalles":

    st.subheader("Ubicacion")
    st.markdown("""<iframe src="https://www.google.com/maps/embed?pb=!1m14!1m12!1m3!1d1145.4788238030683!2d-99.17488306338723!3d19.51721351227803!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!5e0!3m2!1ses!2smx!4v1716911385713!5m2!1ses!2smx" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>""", unsafe_allow_html=True)


    st.subheader("Horarios")
    dia, hora = st.columns(2)
    dia.text("Lunes")
    hora.text("10:00 - 19:00")
    dia.text("Martes")
    hora.text("10:00 - 19:00")
    dia.text("Miercoles")
    hora.text("10:00 - 19:00")
    dia.text("Jueves")
    hora.text("10:00 - 19:00")
    dia.text("Viernes")
    hora.text("10:00 - 19:00")
    dia.text("Sabado")
    hora.text("10:00 - 15:00")

    st.subheader("Contacto")
    st.text("📞 5611922947")

elif selected == "Pistas":
    st.image("assets/pista1.jpeg", width= 500, caption="Esta es nuestra pista 1")
    st.image("assets/pista2.jpeg", width=500,  caption="Esta es nuestra pista 2")

else:
    st.subheader("Reservar")
    c1, c2 = st.columns(2)

    nombre = c1.text_input("Tu nombre*")
    email = c2.text_input("Tu email*")
    fecha =  c1.date_input("Feccha*")
    hora =  c2.selectbox("Hora", horas)
    pista =  c1.selectbox("Pista", pistas)
    notas = c2.text_area("Notas", placeholder="Opcional")

    enviar = st.button("Reservar")

    if enviar:
        with st.spinner("Cargando ...."):
            if nombre == "":
                st.warning("El nombre es oblogatorio")
            elif email == "":
                st.warning("El correo es oblogatorio")
            elif not validate_email(email):
                st.warning("El email no es valido")
            else:
                uid = generate_uid()
                data = [[nombre, email, pista, str(fecha), hora, notas, uid]]
                gs = GoogleSheets(credentials, document, sheet)
                range = gs.get_last_row_range()
                gs.write_data(range, data)


                # Realizamos envio correo de confirmacion
                send(email, nombre, fecha, hora, pista)
                st.success("Su pista ha sido reservada exitosamente.")
