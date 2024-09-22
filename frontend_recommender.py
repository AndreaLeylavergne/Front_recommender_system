import streamlit as st
import pandas as pd
import requests
from io import StringIO

# Charger les identifiants utilisateurs depuis le fichier CSV
# URL du fichier CSV sur Azure Blob Storage
csv_url = "https://functiondef2.blob.core.windows.net/stockblobrecommender/user_recommendations_last.csv?sp=racw&st=2024-09-18T14:04:04Z&se=2027-09-11T22:04:04Z&sv=2022-11-02&sr=b&sig=KrwYchaiGKoBO02dbDqArhJMBjq3gRiJVtSMNL4%2ByvA%3D"

# Charger les identifiants utilisateurs depuis le fichier CSV distant
try:
    response = requests.get(csv_url)
    response.raise_for_status()  # Vérifie que la requête est réussie
    csv_data = StringIO(response.text)  # Convertit le texte en objet compatible avec pandas
    df = pd.read_csv(csv_data)
    id_clients = df['user_id'].unique().tolist()
except requests.exceptions.RequestException as e:
    st.error(f"Erreur lors du chargement du fichier CSV : {e}")
    st.stop()

# Titre de l'application
st.title("Système de Recommandation de Livres")

# Message d'accueil
st.write("Bonjour cher utilisateur ! Choisissez dans le menu déroulant votre identifiant et nous vous recommanderons les ouvrages qui vous correspondent le mieux pour cette saison.")

# Menu déroulant pour choisir l'id utilisateur
id_utilisateur = st.selectbox("Choisissez votre identifiant", id_clients)

# Bouton pour obtenir des recommandations
if st.button("Obtenir des recommandations"):
    st.write("Requête en cours...")

    # Appel à l'API serverless pour obtenir les recommandations
    try:
        # Utilisation de 'user_id' au lieu de 'id_utilisateur'
        url = f"https://functiondef.azurewebsites.net/api/get_recommendations?user_id={id_utilisateur}"
        response = requests.get(url)
        st.write(f"Réponse du serveur : {response.status_code}")

        if response.status_code == 200:
            recommendations = response.json()
            st.write("Voici les titres que nous avons trouvés pour vous. Nous espérons que vous allez en profiter :")
            for title in recommendations:
                st.write(f"- {title}")
        else:
            st.write("Aucune recommandation trouvée pour cet utilisateur.")
    except Exception as e:
        st.write(f"Erreur lors de la requête : {e}")

# Footer de l'application
st.write("Merci d'utiliser notre système de recommandation de livres !")
