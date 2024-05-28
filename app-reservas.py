import streamlit as st
from streamlit_option_menu import option_menu


# Variables
page_title = "Club de padel"
page_icon = "🎾"
layout = "centered"

horas = ["12:00", "17:00", "18:00"]
pistas = ["Pista 1", "Pista2"]



st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)


# Diseño de la pagina
st.image("assets/padel.jpeg")
st.title("Club de padel")
st.text("Direccion del establecimiento")

selected = option_menu(menu_title=None, options=["Reservar", "Pistas", "Detalles"], icons=["calendar-date", "building", "clipboard-minus"], orientation="horizontal")


if selected == "Detalles":
    st.image("assets/maps.jpg")
    st.markdown("Pulsa [aqui](https://www.google.com.mx/maps/@19.5178532,-99.1753269,16.87z?entry=ttu) para ver la direccion ")

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
    nota = c2.text_area("Notas", placeholder="Opcional")

    enviar = st.button("Reservar")

    if enviar:
        if nombre == "":
            st.warning("El nombre es oblogatorio")
        elif email == "":
            st.warning("El correo es oblogatorio")
        else:
            st.success("Su pista ha sido reservada exitosamente.")
