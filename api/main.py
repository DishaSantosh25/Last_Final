import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

# Custom CSS Styling
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #ffffff; }

    /* Header styling */
    .header {
        background-color: #E5C07B;
        border-radius: 24px;
        padding: 2rem;
        position: relative;
        overflow: hidden;
        margin: 1rem;
    }

    /* Green action buttons */
    .action-btn {
        background-color: #98C379 !important;
        color: white !important;
        border-radius: 16px !important;
        padding: 16px 20px !important;
        margin: 1rem 0 !important;
        width: 100%;
        transition: transform 0.2s;
    }
    .action-btn:hover {
        transform: scale(1.02);
    }

    /* Icon styling */
    .material-icons { vertical-align: middle; }

    /* Back button styling */
    .back-btn {
        color: rgba(0, 0, 0, 0.7) !important;
        font-family: 'Roboto' !important;
        margin: 1rem 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# TensorFlow Model Prediction Function
def model_prediction(test_image):
    model = tf.keras.models.load_model("./wheat.h5")
    image = Image.open(test_image).resize((128, 128))
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr])
    predictions = model.predict(input_arr)
    return np.argmax(predictions)

# Main App
def main():
    # Navigation Back Button
    st.markdown("""
    <div style="margin: 1rem;">
        <button class="back-btn" onclick="window.history.back()">
            ← back
        </button>
    </div>
    """, unsafe_allow_html=True)

    # Header Section
    st.markdown("""
    <div class="header">
        <div style="position: absolute; top: 50px; left: 24px;">
            <h1 style="color: white; font-size: 32px; margin: 0;">Wheat Leaf</h1>
            <p style="color: white; font-size: 24px; margin: 4px 0 0 0;">Identifier</p>
        </div>
        <img src="https://i.ibb.co/7Y6D5jz/wheat.png" 
             style="position: absolute; right: -20px; height: 200px;">
    </div>
    """, unsafe_allow_html=True)

    # Logo and Description
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <img src="https://i.ibb.co/0jQ7ZHz/logo.png" height="70">
        <p style="color: rgba(0, 0, 0, 0.7); font-size: 16px; line-height: 1.5;">
            Supporting Farmers in<br>Safeguarding their Crop Health
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Image Upload Section
    uploaded_file = st.file_uploader("", type=["jpg", "png"], accept_multiple_files=False, key="uploader")

    # Action Buttons
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <label class="action-btn">
            📸 Take picture
            <input type="file" hidden name="camera" accept="image/*" capture="environment">
        </label>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <label class="action-btn">
            🖼️ Import
            <input type="file" hidden name="gallery" accept="image/*">
        </label>
        """, unsafe_allow_html=True)

    # Prediction Logic
    if uploaded_file is not None:
        st.image(uploaded_file, use_column_width=True)
        
        if st.button("Predict Disease"):
            st.snow()
            result_index = model_prediction(uploaded_file)
            class_names = ["Brown_rust", "Healthy", "Loose_Smut", "Yellow_rust", "septoria"]
            st.success(f"**Prediction:** {class_names[result_index]}")

if __name__ == "__main__":
    main()