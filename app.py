import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from model_page import UFCModelPredictor

def show_home():
    st.title("Welcome to the UFC Prediction Tool!")
    st.header("By: Varun, Akshaj, Devon, Bhavesha, Ayush, Aditya, Aashritha, and Luis")

def show_model_page():
    st.title("UFC Prediction Tool 🥊")
    
    # Load and display markdown file
    with open("model_info.md", "r") as f:
        md_content = f.read()
    st.markdown(md_content)
    
    predictor = UFCModelPredictor(file_path='finalufcdataset.csv')
    predictor.load_and_prepare_data()
    predictor.test_models()
    #st.write(f'Best Model: {predictor.best_model} with Accuracy: {predictor.results[predictor.best_model]:.4f}')

def show_prediction_page():
    st.title("Fight Prediction")

    fighter_names = [
        "B.J. Penn", "Royce Gracie", "Antonio Rodrigo Nogueira", "Dominick Cruz", "Max Holloway",
        "Junior Dos Santos", "Frankie Edgar", "Henry Cejudo", "Michael Bisping", "Randy Couture",
        "Kamaru Usman", "Alistair Overeem", "Dan Henderson", "Matt Hughes", "Chuck Liddell",
        "José Aldo", "Conor McGregor", "Israel Adesanya", "Khabib Nurmagomedov",
        "Demetrious Johnson", "Daniel Cormier", "Stipe Miocic", "Georges St-Pierre",
        "Jon Jones", "Anderson Silva", "Bhavesha", "Devon"
    ]
    fighter_attributes = ["Height", "Weight", "Reach"]
    
    fighters = pd.DataFrame(fighter_names)

    predictor = UFCModelPredictor(file_path='finalufcdataset.csv')
    predictor.load_and_prepare_data()
    predictor.test_models(silent=True) 
    

    # Fighter selection
    fighters = predictor.fighters

    col1, col2 = st.columns(2)

    with col1:
        fighter_r_name = st.selectbox("Select Red Fighter", options=fighter_names)

        if fighter_r_name == "Devon":
            fighter_r_index = fighter_names.index("Jon Jones")
        elif fighter_r_name == "Bhavesha":
            fighter_r_index = fighter_names.index("Henry Cejudo")
        else:
            fighter_r_index = fighter_names.index(fighter_r_name)
        
        fighter_r = fighters.iloc[fighter_r_index].values[:15].tolist()
        st.image(f'ufc_images/{fighter_r_name}.png',  width=300)
        st.write("Adjust Red Fighter's Attributes")
        fighter_r[0] = st.slider(f'Attribute {fighter_attributes[0]} cm', min_value=0, max_value=400, value=int(fighter_r[3]))
        fighter_r[1] = st.slider(f'Attribute {fighter_attributes[1]} cm', min_value=0, max_value=200, value=int(fighter_r[4]))
        fighter_r[2] = st.slider(f'Attribute {fighter_attributes[2]} cm', min_value=0, max_value=400, value=int(fighter_r[5]))
    with col2:
        fighter_b_name = st.selectbox("Select Blue Fighter", options=fighter_names)
        if fighter_b_name == "Devon":
            fighter_b_index = fighter_names.index("Jon Jones")
        elif fighter_b_name == "Bhavesha":
            fighter_b_index = fighter_names.index("Henry Cejudo")
        else:
            fighter_b_index = fighter_names.index(fighter_b_name)
        #fighter_b_index = st.selectbox("Select Blue Fighter", options=range(len(fighter_names)), format_func=lambda x: fighter_names[x])
        #fighter_b_index = fighter_names.index(fighter_b_name)
        fighter_b = fighters.iloc[fighter_b_index].values[:15].tolist()
        #print(fighter_b_name)
        st.image(f'ufc_images/{fighter_b_name}.png', width = 300)  # Replace with actual image path
        #print(fighter_b)
        st.write("Adjust Blue Fighter's Attributes")
        # for i, _ in enumerate(fighter_b):
        #     attr = fighter_b[i+3]
        #     if isinstance(attr, (int, float)):
        #         if i < 3:
        #             fighter_b[i] = st.slider(f'Attribute {fighter_attributes[i]}', min_value=0, max_value=200, value=int(attr), key=f'blue_{i}')
        fighter_b[0] = st.slider(f'Attribute {fighter_attributes[0]} cm', min_value=0, max_value=400, value=int(fighter_b[3]), key=f'blue_{0}')
        fighter_b[1] = st.slider(f'Attribute {fighter_attributes[1]} cm', min_value=0, max_value=200, value=int(fighter_b[4]), key=f'blue_{1}')
        fighter_b[2] = st.slider(f'Attribute {fighter_attributes[2]} cm', min_value=0, max_value=400, value=int(fighter_b[5]), key=f'blue_{2}')

    if st.button('Predict Winner'):
        combined_features = fighter_r + fighter_b  # Ensure we have 30 features
        if len(combined_features) == 30:
            winner = predictor.predict_winner(fighter_r, fighter_b)
            if winner == fighter_r:
                st.write(f'The predicted winner is: {fighter_r_name}')
            else:
                st.write(f'The predicted winner is: {fighter_b_name}')

        else:
            st.write(f"Error: Combined features length is {len(combined_features)}, expected 30.")

def main():
    # Navigation bar
    selected = option_menu(
        menu_title=None,  # required
        options=["Home", "Model Page", "Prediction"],  # required
        icons=["house", "bar-chart", "bullseye"],  # optional
        menu_icon="cast",  # optional
        default_index=0,  # optional
        orientation="horizontal",
    )

    if selected == "Home":
        show_home()
    elif selected == "Model Page":
        show_model_page()
    elif selected == "Prediction":
        show_prediction_page()

if __name__ == "__main__":
    main()
