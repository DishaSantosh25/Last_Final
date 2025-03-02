import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import base64

# Page configuration
st.set_page_config(
    page_title="Wheat Leaf Identifier",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Base64 encoded wheat image
WHEAT_IMAGE = """
data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTI4IiBoZWlnaHQ9IjEyOCIgdmlld0JveD0iMCAwIDI0IDI0IiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxwYXRoIGQ9Ik0xMiAyQzYuNDggMiAyIDYuNDggMiAxMnM0LjQ4IDEwIDEwIDEwIDEwLTQuNDggMTAtMTBTMTcuNTIgMiAxMiAyem0tMSAxNS45M0M3LjA1IDE3LjQzIDQgMTQuOTcgNCAxMmMwLTQuNDIgMy41OC04IDgtOHM4IDMuNTggOCA4YzAgMi45Ny0zLjA1IDUuNDMtNyA1Ljkzdi0xMS45YzAtLjU1LS40NS0xLTEtMXMtMSAuNDUtMSAxdjExLjl6IiBmaWxsPSIjZmZmZmZmIiBmaWxsLW9wYWNpdHk9IjAuMyIvPjwvc3ZnPg==
"""

# Custom CSS
st.markdown("""
<style>
    /* Global Styles */
    [data-testid="stAppViewContainer"] {
        background-color: #FFFFFF;
    }
    
    /* Header Banner */
    .header-banner {
        background: linear-gradient(135deg, #F5C06B 0%, #F9D69B 100%);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    
    /* Wheat Image Styling */
    .wheat-image {
        position: absolute;
        left: 0;
        top: 50%;
        transform: translateY(-50%);
        width: 120px;
        height: 120px;
        opacity: 0.6;
        mix-blend-mode: soft-light;
        object-fit: cover;
    }
    
    /* Banner Content */
    .banner-content {
        position: relative;
        z-index: 1;
        margin-left: 100px;
    }
    
    .title-text {
        color: #FFFFFF;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .title-text h1 {
        font-size: 2.5em;
        font-weight: 800;
        margin: 0;
        line-height: 1.1;
    }
    
    .title-text h2 {
        font-size: 1.8em;
        font-weight: 600;
        margin: 0;
        opacity: 0.9;
    }
    
    /* Button Styling */
    .stButton > button {
        background-color: #92C756 !important;
        color: white !important;
        font-size: 16px !important;
        padding: 16px 24px !important;
        border-radius: 12px !important;
        border: none !important;
        width: 100% !important;
        margin: 8px 0 !important;
    }
    
    .stButton > button:hover {
        background-color: #7DAD48 !important;
        border: none !important;
    }
    
    /* Center Section */
    .center-section {
        text-align: center;
        padding: 1rem 0 2rem 0;
    }
    
    .leaf-icon {
        color: #92C756;
        font-size: 2.5em;
        margin-bottom: 1rem;
    }
    
    .subtitle {
        color: #4A4A4A;
        font-size: 1.2em;
        line-height: 1.5;
        margin: 0.5rem 0;
        font-weight: 500;
    }
    
    /* Hide default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Hide default file uploader */
    [data-testid="stFileUploadDropzone"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# TensorFlow Model Functions
@st.cache_resource
def load_model():
    return tf.keras.models.load_model("./wheat.h5")

def model_prediction(image_data):
    model = load_model()
    image = Image.open(image_data)
    image = image.resize((128, 128))
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr])
    predictions = model.predict(input_arr)
    return np.argmax(predictions)

# Header Banner with Wheat Image
st.markdown("""
    <div class="header-banner">
        <img src="wheat.jpg" class="wheat-image" alt="Wheat"/>
        <div class="banner-content">
            <div class="title-text">
                <h1>Wheat Leaf</h1>
                <h2>Identifier</h2>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Center Section
st.markdown("""
    <div class="center-section">
        <div class="leaf-icon">🌿</div>
        <div class="subtitle">
            Supporting Farmers in Safeguarding their Crop Health
        </div>
    </div>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_view' not in st.session_state:
    st.session_state.current_view = None

# Create columns for better layout
col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    # Direct button implementation
    camera_btn = st.button("📸 Take picture of your plant")
    gallery_btn = st.button("🖼️ Import from your gallery")

    # Handle button clicks
    if camera_btn:
        st.session_state.current_view = 'camera'
    if gallery_btn:
        st.session_state.current_view = 'gallery'

    # Show appropriate view based on button clicks
    if st.session_state.current_view == 'camera':
        camera_input = st.camera_input("")
        if camera_input:
            st.image(camera_input)
            if st.button("Analyze Image", key="analyze_camera"):
                with st.spinner("📊 Analyzing your wheat leaf..."):
                    st.snow()
                    result_index = model_prediction(camera_input)
                    class_names = ["Brown_rust", "Healthy", "Loose_Smut", "Yellow_rust", "septoria"]
                    if class_names[result_index] == "Healthy":
                        st.success("✨ Your wheat plant is healthy!")
                        st.balloons()
                    else:
                        st.warning(f"⚠️ Disease Detected: {class_names[result_index]}")
                        st.info("💡 Recommendation: Consult with an agricultural expert for treatment options.")

    elif st.session_state.current_view == 'gallery':
        uploaded_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'])
        if uploaded_file:
            st.image(uploaded_file)
            if st.button("Analyze Image", key="analyze_upload"):
                with st.spinner("📊 Analyzing your wheat leaf..."):
                    st.snow()
                    result_index = model_prediction(uploaded_file)
                    class_names = ["Brown_rust", "Healthy", "Loose_Smut", "Yellow_rust", "septoria"]
                    if class_names[result_index] == "Healthy":
                        st.success("✨ Your wheat plant is healthy!")
                        st.balloons()
                    else:
                        st.warning(f"⚠️ Disease Detected: {class_names[result_index]}")
                        st.info("💡 Recommendation: Consult with an agricultural expert for treatment options.") 