import streamlit as st 

def bienvenida(nombre):
    mymensaje = 'Bienvenido/a : ' + nombre
    return mymensaje

myname = st.text_input('Nombre : ')

if (myname):
    mensaje = bienvenida(myname)
    st.write(f' Resultado -> {mensaje}')