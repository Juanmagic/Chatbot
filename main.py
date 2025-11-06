#LIBRERIAS
import streamlit as st
import groq

#VARIABLES
altura_contenedor_chat = 600
stream_status = True

#CONSTANTES
MODELOS = ["llama-3.1-8b-instant", "llama-3.3-70b-versatile", "llama-guard-4-12b"]

#FUNCIONES

#ESTA FUNCIÓN UTILIZA STREAMLIT PARA CREAR LA INTERFAZ DE LA PÁGINA Y ADEMÁS RETORNA El
#MODELO ELEGIDO POR EL USUARIO
def configurar_pagina():

    st.set_page_config(page_title="El chat de juan", page_icon= "😎")

    st.title("El Chat de juan prueba")

    st.sidebar.title("Seleccion de modelos")

    elegirModelo = st.sidebar.selectbox("Elegí un modelo", options=MODELOS, index=0)

    return elegirModelo

#ESTA FUNCION LLAMA A st.secrets PARA OBTENER LA CLAVE DE LA API DE GROQ Y CREA UN USUARIO
def crear_usuario():    
    clave_secreta = st.secrets["CLAVE_API"]
    return groq.Groq(api_key = clave_secreta)

#CONFIGURA EL MODELO DE LENGUAJE PARA QUE PROCESE EL PROMPT DEL USUARIO
def configurar_modelo(cliente, modelo_elegido, prompt_usuario):
    return cliente.chat.completions.create(
        model = modelo_elegido,
        messages = [{"role" : "user", "content" : prompt_usuario}],
        stream = stream_status
    )

#CREAMOS UNA SESION LLAMADA "mensajes" QUE VA A GUARDAR LO QUE LE ESCRIBIMOS AL CHATBOT
def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role" : rol, "content" : contenido, "avatar" : avatar})

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
            st.write(mensaje["content"])

def area_chat():
    contenedor = st.container(height=altura_contenedor_chat, border=True)
    with contenedor:
        mostrar_historial()

def generar_respuesta(respuesta_completa_del_bot):
    _respuesta_posta = ""
    for frase in respuesta_completa_del_bot:
        if frase.choices[0].delta.content:
            _respuesta_posta += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return _respuesta_posta
