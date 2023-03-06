# Activate virtual env
source streamlit-env/bin/activate

# Run hello_world.py
streamlit run app-firestore.py --server.enableCORS false --server.enableXsrfProtection false
 