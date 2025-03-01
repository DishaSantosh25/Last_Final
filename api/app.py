import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import io

# Custom CSS for styling
st.markdown("""
<style>
    /* Header Card Styling */
    .header-card {
        background-color: #F9D69B;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 30px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .header-text {
        color: #2C3333;
    }
    .header-text h1 {
        font-size: 2.5em;
        margin: 0;
        font-weight: bold;
    }
    
    /* Center Section Styling */
    .center-section {
        text-align: center;
        margin: 30px 0;
    }
    .subtitle {
        font-size: 1.2em;
        color: #2C3333;
        margin: 15px 0;
    }
    
    /* Button Styling */
    .custom-button {
        background-color: #92C756;
        color: white;
        padding: 15px 20px;
        border-radius: 10px;
        text-align: center;
        margin: 10px 0;
        cursor: pointer;
        width: 100%;
        border: none;
        font-size: 1.1em;
    }
    .custom-button:hover {
        background-color: #7DAD48;
    }
    
    /* Icon Styling */
    .icon {
        font-size: 2em;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# TensorFlow Model Prediction Function
@st.cache_resource
def load_model():
    return tf.keras.models.load_model("./wheat.h5")

def model_prediction(image_data):
    model = load_model()
    # Convert uploaded image to PIL Image
    image = Image.open(image_data)
    # Resize image
    image = image.resize((128, 128))
    # Convert to array and preprocess
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr])  # Convert single image to batch
    # Get predictions
    predictions = model.predict(input_arr)
    return np.argmax(predictions)

# Header Card
st.markdown("""
    <div class="header-card">
        <div class="header-text">
            <h1>Wheat Leaf</h1>
            <h1>Identifier</h1>
        </div>
        <div>
            🌾
        </div>
    </div>
""", unsafe_allow_html=True)

# Center Section
st.markdown("""
    <div class="center-section">
        <div class="icon">🌿</div>
        <div class="subtitle">
            Supporting Farmers in Safeguarding their Crop Health
        </div>
    </div>
""", unsafe_allow_html=True)

# Create columns for better layout
col1, col2, col3 = st.columns([1,3,1])

with col2:
    # Camera Input
    camera_input = st.camera_input("Take a picture")
    
    # File Upload
    uploaded_file = st.file_uploader("Or choose from gallery", type=['png', 'jpg', 'jpeg'])
    
    # Process either camera input or uploaded file
    image_data = camera_input if camera_input is not None else uploaded_file
    
    if image_data is not None:
        # Display the image
        st.image(image_data, use_column_width=True)
        
        # Predict button
        if st.button("Predict", key="predict_button"):
            with st.spinner("Analyzing image..."):
                st.snow()  # Visual effect
                # Get prediction
                result_index = model_prediction(image_data)
                # Class names
                class_names = ["Brown_rust", "Healthy", "Loose_Smut", "Yellow_rust", "septoria"]
                # Display result
                st.success(f"Prediction: {class_names[result_index]}")
                
                # Additional information based on prediction
                if class_names[result_index] == "Healthy":
                    st.balloons()
                    st.markdown("✅ Your wheat plant appears to be healthy!")
                else:
                    st.warning(f"Disease detected: {class_names[result_index]}")
                    st.info("Consider consulting with an agricultural expert for treatment options.")
    else:
        st.info("Please take a picture or upload an image to begin analysis.") 