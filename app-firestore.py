import streamlit as st
import pandas as pd 
from google.cloud import firestore

db=firestore.Client.from_service_account_json('bruno-demo2-firebase-adminsdk-gsfo7-5d00cefefe.json')
dbNames=db.collection('names')

st.header('Nuevo Registro')

index=st.text_input('Index: ')
name=st.text_input('Name : ')
sex=st.selectbox('Select sex',('F','M','Otro'))

submit=st.button('Crear nuevo registro')

#CREATE

if index and name and sex and submit:
    doc_ref=db.collection('names').document(name)
    doc_ref.set({
        'index': index,
        'name': name,
        'sex': sex
    })
    st.sidebar.write('Registro insertado correctamente')

names_ref=list(db.collection(u'names').stream())
names_dict=list(map(lambda x:x.to_dict(),names_ref))
names_dataframe=pd.DataFrame(names_dict)
st.dataframe(names_dataframe)

#Buscar

def loadByName(name):
    names_ref=dbNames.where(u'name',u'==',name)
    currentName=None
    for myname in names_ref.stream():
        currentName=myname
    return currentName


st.sidebar.subheader('Buscar Nombre')
nameSearch=st.sidebar.text_input('nombre')
btnFiltrar=st.sidebar.button('Buscar')

if nameSearch and btnFiltrar:
    doc=loadByName(nameSearch)
    if doc is None:
        st.sidebar.write('Nombre no existe')
    else:
        st.sidebar.write(doc.to_dict())


st.sidebar.markdown('''---''')
btnEliminar=st.sidebar.button('Eliminar')

if btnEliminar:
    deletename = loadByName(nameSearch)
    if deletename is None:
        st.sidebar.write(f'{nameSearch} no existe')
    else:
        dbNames.document(deletename.id).delete()
        st.sidebar.write(f'{nameSearch} eliminado')

st.sidebar.markdown('''---''')
newname=st.sidebar.text_input('Actualizar nombre')
btnActualizar=st.sidebar.button('Actualizar')

if btnActualizar:
    updatename=loadByName(nameSearch)
    if updatename is None:
        st.sidebar.write(f'{nameSearch} no existe')
    else:
        myupdatename=dbNames.document(updatename.id)
        myupdatename.update(
            {
                'name':newname
            }
        )
        st.sidebar.write(f'{nameSearch} actualizado con {newname}')
