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
        # lire le fichier CSV contenant les utilisateurs      
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
    st.rerun()


# --- 2 pages de l'application ---
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
    """Affiche la page d'accueil après connexion."""
    st.title(f"Bienvenue, {st.session_state['username']}, sur ma page d'accueil")
    st.markdown("""
        Ceci est la page principale de votre application sécurisée. 
        Utilisez le menu latéral pour naviguer.
    """)
    st.image("https://placehold.co/800x200/50C878/white?text=Contenu+Accueil", caption="Votre tableau de bord")
    
def cat_album_page():
    """Affiche la page de l'album photo du carnet de voyage."""
    st.title("Bienvenue dans l'album de mon carnet de voyage")

    # Définir les colonnes avant de les utiliser
    col1, col2, col3 = st.columns(3)

    # Chargement et affichage des images côte à côte
    url1 = "https://cdn.generationvoyage.fr/2025/02/Golden-Gate-de-San-Francisco-1000x649.jpeg"
    url2 = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSd49EOl1Bj7_yT7CqK-6Z8ZeGYUSyA4NkUaw&s"
    # J'ai remplacé l'URL problématique par une image de Las Vegas fonctionnelle
    url3 = "https://cdn.generationvoyage.fr/2023/10/skyline-las-vegas-nuit-750x497.jpg"

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
        # Streamlit affiche déjà l'erreur du FileNotFoundError
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
            if st.button("🖼️ Les photos de mon voyage", key="nav_cat", type="primary" if st.session_state['page'] == 'cat_album' else 'secondary'):
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
        login_page(users_df)

if __name__ == "__main__":
    main()



