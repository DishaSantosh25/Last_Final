import streamlit as st
import tensorflow as tf
import numpy as np

# TensorFlow Model Prediction Function
def model_prediction(test_image):
    # Load the model (ensure the model file is in the correct path)
    model = tf.keras.models.load_model("./wheat.h5")
    # Load and preprocess the image from the uploaded file
    image = tf.keras.preprocessing.image.load_img(test_image, target_size=(128, 128))
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr])  # convert single image to batch format
    predictions = model.predict(input_arr)
    return np.argmax(predictions)  # return index of highest prediction

# Set page configuration (optional)
st.set_page_config(page_title="Disease Recognition", layout="centered")

# --- Custom CSS Styling ---
st.markdown(
    """
    <style>
    /* Overall page background */
    [data-testid="stAppViewContainer"] {
        background-color: #f5f5f5;
    }
    /* Header styling */
    .header {
        font-size: 32px;
        font-weight: bold;
        color: #2c3e50;
        text-align: center;
        padding: 20px;
    }
    /* Uploader container styling */
    .uploader {
        background-color: #ffffff;
        padding: 20px;
        border: 2px dashed #ddd;
        border-radius: 10px;
        text-align: center;
        margin: 20px auto;
        width: 50%;
    }
    /* Button styling */
    .stButton>button {
        padding: 10px 24px;
        font-size: 16px;
        border-radius: 8px;
    }
    /* Specific button colors */
    .show-btn {
        background-color: #2980b9;
        color: white;
    }
    .predict-btn {
        background-color: #27ae60;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Page Content ---
# Styled header
st.markdown('<div class="header">Disease Recognition</div>', unsafe_allow_html=True)

# Uploader area
st.markdown('<div class="uploader">', unsafe_allow_html=True)
test_image = st.file_uploader("Choose an Image:", type=["png", "jpg", "jpeg"])
st.markdown('</div>', unsafe_allow_html=True)

# Check if an image is uploaded
if test_image is not None:
    # Display "Show Image" button and show the uploaded image when clicked
    if st.button("Show Image", key="show"):
        st.image(test_image, use_column_width=True)

    # Display "Predict" button and run model prediction when clicked
    if st.button("Predict", key="predict"):
        st.snow()  # decorative effect
        st.write("Our Prediction:")
        result_index = model_prediction(test_image)
        # Define class names corresponding to model output indices
        class_name = ["Brown_rust", "Healthy", "Loose_Smut", "Yellow_rust", "septoria"]
        st.success("Model is predicting it's a {}".format(class_name[result_index]))
else:
    st.info("Please upload an image to begin.")
