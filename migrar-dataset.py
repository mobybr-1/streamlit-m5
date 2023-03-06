import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd

path = "./" 

cred = credentials.Certificate(path +"bruno-demo2-firebase-adminsdk-gsfo7-5d00cefefe.json") 
firebase_admin.initialize_app(cred)

db = firestore.client()
doc_ref = db.collection(u'profesores') # Set the name of the Collection
# Import data
df = pd.read_csv(path+'profesores.csv')
tmp = df.to_dict(orient='records')
list(map(lambda x: doc_ref.add(x), tmp))