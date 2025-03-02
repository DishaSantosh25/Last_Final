import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import io

# Page configuration
st.set_page_config(
    page_title="Wheat Leaf Identifier",
    layout="centered",
    initial_sidebar_state="collapsed"
)

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
    
    .banner-content {
        display: flex;
        align-items: center;
        justify-content: space-between;
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
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Hide default file uploader */
    [data-testid="stFileUploadDropzone"] {
        display: none;
    }
    
    /* Custom button styling */
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
    
    /* Image display styling */
    [data-testid="stImage"] img {
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Container for buttons */
    .button-container {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        margin: 1rem 0;
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

# Header Banner
st.markdown("""
    <div style="background: linear-gradient(135deg, #F5C06B 0%, #F9D69B 100%); padding: 20px; border-radius: 20px; margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h1 style="color: white; margin: 0; font-size: 2.5em; font-weight: 800;">Wheat Leaf</h1>
                <h2 style="color: white; margin: 0; font-size: 1.8em; font-weight: 600; opacity: 0.9;">Identifier</h2>
            </div>
            <div style="font-size: 2.5em;">🌾</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Center Section
st.markdown("""
    <div style="text-align: center; margin: 20px 0;">
        <div style="font-size: 2.5em; color: #92C756; margin-bottom: 10px;">🌿</div>
        <div style="font-size: 1.2em; color: #4A4A4A; line-height: 1.5;">
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