import pandas as pd
import numpy as np
import streamlit as st

#streamlit run .\OSF_Streamlit.py

#---PAGE CONFIG---
#To Do: Hacer el page config bonito
st.title("Dashboard de Estudiantes por OSF")
sidebar = st.sidebar
sidebar.title("Barra de opciones")

#---READ DATA---
@st.cache
def load_data():
    data=pd.read_excel("Machote Inscripciones.xlsx",sheet_name="ListadoCompleto")
    data=data.drop(["En cuantos proyectos esta el alumno","Unnamed: 3","Plan de estudios"],axis=1) #Borrar columnas extras
    return data

data_load_state=st.text("Loading data...")
data=load_data()
data_load_state.text("")

#---FILTROS---
sidebar.write("Seleccione filtros deseados")

#Filtro por OSF
OSFname=sidebar.selectbox("Seleccionar OSF:", 
                            data['Organización SF'].unique())
OSFdata=data[data["Organización SF"]==OSFname] #Filtra experiencias por OSF
#Initialising SessionState's
if OSFdata not in st.session_state:
    st.session_state.load_state = False

#Filtro de experiencias de OSF
with st.sidebar.form(key="my_form"):
    OSFexp=st.selectbox("Nombre de la experiencia", 
                            options=OSFdata['Nombre experiencia'].unique())
    submit_button=st.form_submit_button(label="Buscar") #Botón 
OSFexpdata=OSFdata[OSFdata["Nombre experiencia"]==OSFexp] #Filtro
OSFexpdata=OSFexpdata.reset_index()
OSFexpdata=OSFexpdata.drop("index",axis=1)
st.sidebar.markdown("##")

#---DEV---(BORRAR)
sidebar.write("DEV BUTTON")
if sidebar.checkbox("Show dataframe"):
    st.dataframe(OSFexpdata)
    st.markdown("##")

#---SELECCION DE DATOS---
#Datos de alumnos deseados
st.subheader("Selección de Datos")
Datos = st.multiselect(label="Puedes omitir los datos que consideres no relevantes",
                            #label_visibility="hidden",
                            options=list(OSFexpdata.columns),
                            default=list(OSFexpdata.columns))
st.markdown("""---""")

#Obtener datos
def GetDataStudent (Col,fila): #Col: seleccionadas de Datos, Fila: estudiantes
    Dic_Datos={}
    for i in Col:
        Dato=OSFexpdata[i][fila] #Dato individual
        Dic_Datos[i]=Dato #Crear Key:Value
    return Dic_Datos

#To Do, hacer una función que imprima cada alumno de forma bonita. USAR st.expander
#Diseño del expander
def GetExpander(dicc):
    my_expander = st.expander(label='Ver Datos')
    with my_expander:
        st.write(dicc)

#---MAIN---
st.subheader("Alumnos")
if submit_button or st.session_state.load_state:
    st.session_state.load_state=True
    #Imprimir Datos por alumno personalizado
    for i in range(OSFexpdata.shape[0]):
        Alumno=GetDataStudent(Datos,i) #Datos en diccionario
        st.write(f"Alumno {i+1}") #Cuando tengamos datos de alumnos: st.write(texto["Nombre Completo del estudiante"])
        GetExpander(Alumno)
    st.markdown("""---""")

    #Salvar datos en excel
    df=pd.DataFrame(OSFexpdata)
    Save_data=st.button("Salvar Datos")
    if Save_data:
        st.write("Done")

    #Dev stuff (BORRAR)
    st.write(Alumno.keys())
