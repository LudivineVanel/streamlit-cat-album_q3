import streamlit as st
import pandas as pd
from PIL import Image

# --- Configuration de la page ---
st.set_page_config(layout="wide", page_title="Bienvenue", page_icon="🏠")

# --- Initialisation de l'état de la session ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = None
if 'page' not in st.session_state:
    st.session_state['page'] = 'login'

# --- 1 FONCTIONS D'AUTHENTIFICATION ---

@st.cache_data
def load_user_data():
    """Charge les données des utilisateurs depuis le fichier CSV."""
    try:
        #lire le fichier CSV contenant les utilisateurs     
        df = pd.read_csv("users.csv")
        df['name'] = df['name'].astype(str).str.strip()
        df['password'] = df['password'].astype(str).str.strip()
        return df
    except FileNotFoundError:
        st.error("Le fichier users.csv est introuvable. Veuillez vous assurer qu'il est dans le même répertoire.")
        return pd.DataFrame()

def authenticate_user(username, password, users_df):
    """Vérifie les informations d'identification de l'utilisateur."""
    # S'assurer que les chaînes sont propres avant la comparaison
    username = username.strip()
    password = password.strip()
    
    # Trouver l'utilisateur correspondant
    user_match = users_df[users_df['name'] == username]

    if not user_match.empty:
        # Le user existe, il vérifie son mdp 
        stored_password = user_match['password'].iloc[0]
        
        if stored_password == password:
            # Succès de l'authentification
            st.session_state['username'] = username
            st.session_state['authenticated'] = True
            st.session_state['page'] = 'home' # Rediriger vers la page d'accueil
            st.rerun()
        else :
            # mdp incorrect
            st.warning("Mot de passe incorrect.")
            return False
    else :
        # utilisateur non trouvé
        st.warning("Nom d'utilisateur ou mot de passe incorrect.")
        return False
        
def logout():
    """Déconnecte l'utilisateur."""
    st.session_state['authenticated'] = False
    st.session_state['username'] = None
    st.session_state['page'] = 'login'
    # st.rerun() est inclus dans la fonction main pour forcer le rafraîchissement
    st.rerun()


# --- 2 pages de l'application ---
# CORRECTION : login_page doit accepter users_df en argument
def login_page(users_df):
    """Affiche la page de connexion."""
    st.title("Login")
    
    # utilisation d'un container pour centrer le formulaire
    with st.container(border=True):
        # création d'un formulaire de connexion
        with st.form("login_form"): 
            username = st.text_input("Username", value ="", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            submit_button = st.form_submit_button("Login")

            if submit_button:
                if username and password:
                    # L'argument users_df est maintenant correctement utilisé
                    authenticate_user(username, password, users_df)
                else:
                    # Rétabli le message d'erreur si les champs sont vides
                    st.warning("Les champs username et mot de passe doivent être remplis")
    
def home_page():
    """Affiche la page d'accueil après connexion (similaire à image_f08af9.jpg)."""
    st.title("Bienvenue sur ma page")
    # Utilisation d'une URL de GIF pour l'exemple
    st.image("data:image/jpeg;base64,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")
    
def cat_album_page():
    """Affiche la page de l'album photo du carnet de voyage."""
    st.title("Bienvenue dans l'album de mon carnet de voyage")

    # Chargement et affichage des images côte à côte
    # J'utilise des URLs ici pour la démonstration :
    url1 = "https://cdn.generationvoyage.fr/2025/02/Golden-Gate-de-San-Francisco-1000x649.jpeg"
    url2 = "data:image/jpeg;base64,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.jpg" 
    url3 = "https://cdn.generationvoyage.fr/2019/04/las_vegas_1555335675-e1555335688841.jpg" 
    
    # Création des colonnes pour aligner 3 images sur la même ligne
    col1, col2, col3 = st.columns(3)

    # Affichage des images dans les colonnes
    with col1:
        st.image(url1, caption="San Francisco", use_column_width="always")
    with col2:
        st.image(url2, caption="Mohab", use_column_width="always")
    with col3:
        st.image(url3, caption="Las Vegas", use_column_width="always")


# --- 3. LOGIQUE PRINCIPALE DE L'APPLICATION ---

def main():
    """Contrôle la structure et le flux de l'application."""
    
    users_df = load_user_data()

    if users_df.empty and st.session_state['page'] == 'login':
        # Si le CSV est vide et qu'on est sur la page de login, on arrête.
        return

    if st.session_state['authenticated']:
        # --- Barre Latérale (Sidebar) pour les Utilisateurs Authentifiés ---
        with st.sidebar:
            st.button("Déconnexion", on_click=logout)
            st.write(f"**Bienvenue {st.session_state['username']}**")
            st.markdown("---")

            # Boutons de navigation (Menu)
            st.subheader("Menu")
            
            # Utilisation de boutons Streamlit pour gérer la navigation
            # Accueil
            if st.button("🏠 Accueil", key="nav_home", type="primary" if st.session_state['page'] == 'home' else 'secondary'):
                st.session_state['page'] = 'home'
                st.rerun()

            # Album Photo
            if st.button("😺 Les photos de mon chat", key="nav_cat", type="primary" if st.session_state['page'] == 'cat_album' else 'secondary'):
                st.session_state['page'] = 'cat_album'
                st.rerun()

        # --- Affichage du Contenu de la Page ---
        if st.session_state['page'] == 'home':
            home_page()
        elif st.session_state['page'] == 'cat_album':
            cat_album_page()
        else:
            # Cas par défaut si l'utilisateur est authentifié mais sans page définie
            home_page()
            
    else:
        # --- Affichage de la Page de Connexion pour les Utilisateurs Non Authentifiés ---
        # L'argument users_df est passé ici
        login_page(users_df)

if __name__ == "__main__":
    main() 



