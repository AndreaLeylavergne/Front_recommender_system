import streamlit as st
import pandas as pd
import requests

# Charger les identifiants utilisateurs depuis le fichier CSV
df = pd.read_csv("user_recommendations_last.csv")
id_clients = df['user_id'].unique().tolist()

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
