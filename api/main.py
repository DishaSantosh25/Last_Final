import streamlit as st
import base64
import tensorflow as tf
import numpy as np
from PIL import Image

# TensorFlow Model Prediction Function
def model_prediction(test_image):
    model = tf.keras.models.load_model("./wheat.h5")
    # Open image using PIL (works for file-like objects)
    image = Image.open(test_image)
    image = image.resize((128, 128))
    input_arr = np.array(image)
    input_arr = np.expand_dims(input_arr, axis=0)  # convert single image to batch format
    predictions = model.predict(input_arr)
    return np.argmax(predictions)  # return index of highest prediction

def main():
    # Configure page
    st.set_page_config(page_title="Wheat Leaf Identifier", layout="centered")

    # Inject custom CSS for layout & styling
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

        /* Button container styling */
        .button-container {
            margin: 16px;
        }
        .custom-button {
            width: 100%; 
            padding: 16px 20px; 
            background-color: #98C379; 
            border: none; 
            border-radius: 16px; 
            cursor: pointer; 
            margin-bottom: 16px;
            display: flex; 
            justify-content: space-between; 
            align-items: center;
        }
        .button-texts {
            display: flex; 
            flex-direction: column;
        }
        .button-title {
            color: white; 
            font-size: 18px; 
            font-weight: 600; 
            font-family: Roboto; 
            margin: 0;
        }
        .button-subtitle {
            color: rgba(255,255,255,0.8); 
            font-size: 14px; 
            font-family: Roboto; 
            margin: 0;
        }
        .button-icon {
            color: white; 
            font-size: 24px;
        }
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

    # Extra vertical spacing
    st.write("")
    st.write("")
    st.write("")

    # Action buttons container
    st.markdown('<div class="button-container">', unsafe_allow_html=True)

    # 1) "Take picture" button -> st.camera_input with prediction functionality
    take_picture = st.button(
        label="",
        key="take_picture_button",
        help="Take picture of your plant",
    )
    st.markdown(
        """
        <div class="custom-button">
            <div class="button-texts">
                <p class="button-title">Take picture</p>
                <p class="button-subtitle">of your plant</p>
            </div>
            <span class="button-icon">&#128247;</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    if take_picture:
        st.write("**Take a photo using your webcam or mobile camera**:")
        pic_file = st.camera_input("Capture an image")
        if pic_file is not None:
            st.image(pic_file, caption="Captured Image")
            # Predict button for captured image (green bar)
            predict_taken = st.button(
                label="",
                key="predict_taken_button",
                help="Predict disease from captured image",
            )
            st.markdown(
                """
                <div class="custom-button">
                    <div class="button-texts">
                        <p class="button-title">Predict</p>
                        <p class="button-subtitle">Identify Disease</p>
                    </div>
                    <span class="button-icon">&#128202;</span>
                </div>
                """,
                unsafe_allow_html=True
            )
            if predict_taken:
                st.snow()  # decorative effect
                st.write("Our Prediction")
                result_index = model_prediction(pic_file)
                class_name = ["Brown_rust", "Healthy", "Loose_Smut", "Yellow_rust", "septoria"]
                st.success("Model is Predicting it's a {}".format(class_name[result_index]))

    # 2) "Import from gallery" button -> st.file_uploader with prediction functionality
    import_picture = st.button(
        label="",
        key="import_button",
        help="Import from your gallery",
    )
    st.markdown(
        """
        <div class="custom-button">
            <div class="button-texts">
                <p class="button-title">Import</p>
                <p class="button-subtitle">from your gallery</p>
            </div>
            <span class="button-icon">&#128247;</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    if import_picture:
        st.write("**Select an image from your device**:")
        uploaded_file = st.file_uploader("Upload Image", type=["png","jpg","jpeg"])
        if uploaded_file is not None:
            st.image(uploaded_file, caption="Uploaded Image")
            # Predict button for uploaded image (green bar)
            predict_import = st.button(
                label="",
                key="predict_import_button",
                help="Predict disease from uploaded image",
            )
            st.markdown(
                """
                <div class="custom-button">
                    <div class="button-texts">
                        <p class="button-title">Predict</p>
                        <p class="button-subtitle">Identify Disease</p>
                    </div>
                    <span class="button-icon">&#128202;</span>
                </div>
                """,
                unsafe_allow_html=True
            )
            if predict_import:
                st.snow()  # decorative effect
                st.write("Our Prediction")
                result_index = model_prediction(uploaded_file)
                class_name = ["Brown_rust", "Healthy", "Loose_Smut", "Yellow_rust", "septoria"]
                st.success("Model is Predicting it's a {}".format(class_name[result_index]))

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
