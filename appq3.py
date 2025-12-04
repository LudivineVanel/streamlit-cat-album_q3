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
    st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNGh1MWtwd2s3cGcxNjVnd2I0NmV6NG42MnM5OWFocThhbXZmZ3JzMyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/l378Bu6AEs3GzHPUQ/giphy.gif",
            caption="Applaudissements de bienvenue")
    
def cat_album_page():
    """Affiche la page de l'album photo du chat (similaire à image_f08aa1.jpg)."""
    st.title("Bienvenue dans l'album de mon chat 😼")

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


