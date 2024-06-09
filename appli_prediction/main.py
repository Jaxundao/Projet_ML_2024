import pickle
import streamlit as st
import pandas as pd

# chemin
model_path = '/mount/src/projet_ml_2024/appli_prediction/model.sav'

# Chargement du modèle XGBoost retenu
with open(model_path, 'rb') as f:
    model = pickle.load(f)
    
# Fonction de prédiction
def prediction(X):
    prediction = model.predict(X)
    probabilities = model.predict_proba(X)

    if prediction[0] == 1:
        result = 'Client désabonné'
    else:
        result = 'Client non désabonné'

    probability = probabilities[0][prediction[0]] * 100
    return result, probability

def main():

    # Code HTML
    html = """
        <style>
            .center {
                text-align: center;
            }
            .custom-font {
                font-family: 'Bodoni MT', serif;
            }
            .small-font {
                font-size: 40px;  
            }
        </style>
        <h1 class="center custom-font small-font" style="color: black;">Prédiction de désabonnement des clients de la banque Fortuneo</h1>
         """
    # Affichage de la mise en forme
    st.markdown(html, unsafe_allow_html=True)

        # Petite description de la page
    st.divider()
    texte = """
   Bienvenue dans notre outil de prédiction de résiliation de comptes clients. 
   Cet outil a été conçu pour vous aider à anticiper et à gérer les désabonnements de vos clients
   vous permettant ainsi d'améliorer leur fidélité et satisfaction. Ce modèle de scoring  
   la probabilité de résiliation ou de non pour chaque client et le classe dans une catégorie (churn ou pas).
   Veuillez renseigner les informations suivantes pour voir les prédictions du modèle (classe et probabilité associée). 
    """

    # Ajouter du style CSS pour centrer le texte
    css_code = """
        <style>
            .justified-text {
                text-align: justify;
            }
        </style>
    """

    # Affichage du texte avec le style CSS
    st.markdown(css_code, unsafe_allow_html=True)
    st.markdown(f'<p class="justified-text">{texte}</p>', unsafe_allow_html=True)
    st.divider()

    # Créer les champs pour entrer les données recquis pour la prédiction
    # Credit score
    CreditScore = st.number_input("Score de Crédit du client", min_value=0)
    # Geography

    Geo = ['France', 'Spain', 'Germany']
    Geography = st.sidebar.selectbox("Sélectionnez la zone", Geo, index=0)

    # Genre
    sexe = ['Male', 'Female']
    Gender = st.sidebar.selectbox("Sélectionnez le genre du client", sexe, index=0)

    # Age
    Age = st.number_input("L'âge du client", min_value=0, max_value=110)

    # Tenure
    Tenure = st.number_input("Le nombre d'année en tant que client de la banque", min_value=0, max_value=30)

    # Balance
    Balance = st.number_input("Solde actuelle du compte", min_value=0)

    # NumOfProducts
    NumOfProducts = st.number_input("Nombre de produits bancaires utilisé par le client", min_value=0, max_value=10)

    # HasCrCard
    cred = ['Oui', 'Non']
    HasCrCard = st.sidebar.selectbox("Le client a t-il une carte de crédit", cred, index=0)
    HasCrCard = 1 if HasCrCard == 'Oui' else 0

    # IsActiveMember
    act = ['Oui', 'Non']
    IsActiveMember = st.sidebar.selectbox("Le client est il membre actif", act, index=0)
    IsActiveMember = 1 if IsActiveMember == 'Oui' else 0

    # EstimatedSalary
    EstimatedSalary = st.number_input("Salaire estimé du client", min_value=0)

    # Effectuer la prédiction avec la fonction définie plus haut (prediction)
    # objet pour stocker le résultat
    pred = ""
    prob = 0
    # Créer le bouton 'Prédiction'
    if st.button("Prédiction"):
        # Récupérer les champs remplie dans la matrice X
        X = pd.DataFrame({
            'CreditScore': [CreditScore],
            'Geography': [Geography],
            'Gender': [Gender],
            'Age': [Age],
            'Tenure': [Tenure],
            'Balance': [Balance],
            'NumOfProducts': [NumOfProducts],
            'HasCrCard': [HasCrCard],
            'IsActiveMember': [IsActiveMember],
            'EstimatedSalary': [EstimatedSalary],
        })

        # Convertir HasCrCard et IsActiveMember en type object pour se conformer au modèle
        X['HasCrCard'] = X['HasCrCard'].astype('object')
        X['IsActiveMember'] = X['IsActiveMember'].astype('object')

        # Effectuer la prédiction avec le modèle
        pred, prob = prediction(X)
        st.success(f'{pred} avec une probabilité de {prob:.2f}%', icon="✅")
if __name__=='__main__':
    main()

