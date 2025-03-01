import streamlit as st
import base64
import tensorflow as tf
import numpy as np
from PIL import Image

# TensorFlow Model Prediction Function
def model_prediction(test_image):
    model = tf.keras.models.load_model("./wheat.h5")
    # Open image using PIL (works with both file-like objects from camera/file uploader)
    image = Image.open(test_image)
    image = image.resize((128, 128))
    input_arr = np.array(image)
    input_arr = np.expand_dims(input_arr, axis=0)  # convert single image to batch format
    predictions = model.predict(input_arr)
    return np.argmax(predictions)  # return index of highest prediction

def main():
    # Configure page
    st.set_page_config(page_title="Wheat Leaf Identifier", layout="centered")

    # Inject custom CSS for layout & styling including custom button styling for clickable green bars
    st.markdown(
        """
        <style>
        /* Hide default Streamlit hamburger menu & footer */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        /* Page background color */
        [data-testid="stAppViewContainer"] {
            background-color: #FFFFFF;
        }

        /* Top bar (mimicking AppBar with 'back' arrow) */
        .top-bar {
            display: flex; 
            align-items: center; 
            padding: 1rem 0; 
            margin-left: 16px;
        }
        .top-bar-icon {
            color: black; 
            font-size: 20px; 
            margin-right: 4px; 
            cursor: pointer;
        }
        .top-bar-text {
            color: rgba(0,0,0,0.7); 
            font-size: 16px; 
            font-family: Roboto;
            cursor: pointer;
        }

        /* Header container (golden wheat background) */
        .header-container {
            position: relative; 
            height: 200px; 
            background-color: #E5C07B; 
            border-radius: 24px; 
            margin: 16px; 
            overflow: hidden;
        }
        .header-text {
            position: absolute; 
            left: 24px; 
            top: 50px;
            color: white; 
            font-family: Roboto;
        }
        .header-title {
            font-size: 32px; 
            font-weight: bold; 
            margin: 0;
        }
        .header-subtitle {
            font-size: 24px; 
            margin: 4px 0 0 0;
        }
        .header-image {
            position: absolute; 
            right: -20px; 
            top: 0; 
            bottom: 0; 
            width: 200px;
        }

        /* Centered section for logo & tagline */
        .center-section {
            text-align: center; 
            margin-top: 5px;
        }
        .center-section p {
            font-size: 16px; 
            color: rgba(0,0,0,0.7); 
            line-height: 1.5; 
            font-family: Roboto;
        }

        /* Custom button styling for clickable green bars */
        .stButton button {
            background-color: #98C379;
            color: white;
            padding: 16px 20px;
            border: none;
            border-radius: 16px;
            cursor: pointer;
            width: 100%;
            text-align: left;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-family: Roboto;
            font-size: 18px;
            font-weight: 600;
            white-space: pre-line;
        }
        .stButton button:focus {outline: none;}
        </style>
        """,
        unsafe_allow_html=True
    )

    # Top bar with "back" arrow
    st.markdown(
        """
        <div class="top-bar">
            <span class="top-bar-icon">&#8592;</span>
            <span class="top-bar-text">back</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Header with wheat background & image
    st.markdown(
        """
        <div class="header-container">
            <div class="header-text">
                <h1 class="header-title">Wheat Leaf</h1>
                <h2 class="header-subtitle">Identifier</h2>
            </div>
            <img src="https://raw.githubusercontent.com/yourrepo/wheat.webp" class="header-image"/>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Logo & tagline
    col1, col2, col3 = st.columns([3,1,3])
    with col2:
        st.image("https://raw.githubusercontent.com/yourrepo/logo.png", width=70)

    st.markdown(
        """
        <div class="center-section">
            <p>Supporting Farmers in<br>Safeguarding their Crop Health</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")
    st.write("")
    st.write("")

    # Disease Recognition Section Header
    st.header("Disease Recognition")

    # ----------------------- Camera Input Section -----------------------
    # The button label uses newline characters to simulate two lines and an icon on the right.
    if st.button("Take picture\nof your plant          📷", key="take_picture_button"):
        st.write("**Take a photo using your webcam or mobile camera**:")
        pic_file = st.camera_input("Capture an image")
        if pic_file is not None:
            st.image(pic_file, caption="Captured Image")
            # Predict button for captured image
            if st.button("Predict\nIdentify Disease          📊", key="predict_taken_button"):
                st.snow()  # decorative effect
                st.write("Our Prediction")
                result_index = model_prediction(pic_file)
                class_name = ["Brown_rust", "Healthy", "Loose_Smut", "Yellow_rust", "septoria"]
                st.success("Model is Predicting it's a {}".format(class_name[result_index]))

    # ----------------------- File Upload Section -----------------------
    if st.button("Import\nfrom your gallery          📷", key="import_button"):
        st.write("**Select an image from your device**:")
        uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
        if uploaded_file is not None:
            st.image(uploaded_file, caption="Uploaded Image")
            # Predict button for uploaded image
            if st.button("Predict\nIdentify Disease          📊", key="predict_import_button"):
                st.snow()  # decorative effect
                st.write("Our Prediction")
                result_index = model_prediction(uploaded_file)
                class_name = ["Brown_rust", "Healthy", "Loose_Smut", "Yellow_rust", "septoria"]
                st.success("Model is Predicting it's a {}".format(class_name[result_index]))

if __name__ == "__main__":
    main()
