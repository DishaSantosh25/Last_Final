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

# Load and encode the wheat image
def get_wheat_image():
    try:
        with open("wheat.jpg", "rb") as f:
            data = f.read()
            encoded = base64.b64encode(data).decode()
            return f"data:image/jpeg;base64,{encoded}"
    except:
        # Fallback to a default wheat emoji if image is not found
        return None

wheat_image = get_wheat_image()

# Custom CSS with dynamic image
st.markdown(f"""
<style>
    /* Global Styles */
    [data-testid="stAppViewContainer"] {{
        background-color: #FFFFFF;
    }}
    
    /* Header Banner */
    .header-banner {{
        background: linear-gradient(135deg, #F5C06B 0%, #F9D69B 100%);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
        min-height: 120px;
        display: flex;
        align-items: center;
    }}
    
    /* Wheat Image Container and Styling */
    .wheat-image-container {{
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 140px;
        overflow: hidden;
    }}
    
    .wheat-image-container::before {{
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        background-image: url('{wheat_image if wheat_image else ""}');
        background-size: cover;
        background-position: center;
        opacity: 0.4;
        mix-blend-mode: multiply;
    }}
    
    /* Banner Content */
    .banner-content {{
        position: relative;
        z-index: 2;
        margin-left: 120px;
        flex: 1;
    }}
    
    .title-text {{
        color: #FFFFFF;
        text-shadow: 0 2px 4px rgba(0,0,0,0.15);
    }}
    
    .title-text h1 {{
        font-size: 2.2em;
        font-weight: 800;
        margin: 0;
        line-height: 1;
        letter-spacing: -0.02em;
    }}
    
    .title-text h2 {{
        font-size: 1.6em;
        font-weight: 600;
        margin: 2px 0 0 0;
        opacity: 0.95;
        letter-spacing: -0.01em;
    }}
    
    /* Disease Result Styling */
    .result-container {{
        margin: 1.5rem 0;
        padding: 1.2rem;
        border-radius: 12px;
        background: #FFFFFF;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }}
    
    .disease-result {{
        padding: 1.2rem;
        border-radius: 10px;
        margin: 0;
        font-weight: 600;
        font-size: 1.3em;
        text-align: center;
        transition: all 0.3s ease;
    }}
    
    .disease-warning {{
        background: linear-gradient(135deg, #FFE4B5 0%, #FFD700 100%);
        color: #B8860B;
        border: 1px solid rgba(218, 165, 32, 0.3);
        box-shadow: 0 2px 12px rgba(218, 165, 32, 0.15);
    }}
    
    .disease-healthy {{
        background: linear-gradient(135deg, #E6FFE6 0%, #98FB98 100%);
        color: #228B22;
        border: 1px solid rgba(34, 139, 34, 0.3);
        box-shadow: 0 2px 12px rgba(34, 139, 34, 0.15);
    }}
    
    /* Button Styling */
    .stButton > button {{
        background-color: #92C756 !important;
        color: white !important;
        font-size: 16px !important;
        padding: 16px 24px !important;
        border-radius: 12px !important;
        border: none !important;
        width: 100% !important;
        margin: 8px 0 !important;
        transition: all 0.3s ease !important;
    }}
    
    .stButton > button:hover {{
        background-color: #7DAD48 !important;
        border: none !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(146, 199, 86, 0.2) !important;
    }}
    
    /* Center Section */
    .center-section {{
        text-align: center;
        padding: 0.5rem 0 1.5rem 0;
    }}
    
    .leaf-icon {{
        color: #92C756;
        font-size: 2.2em;
        margin-bottom: 0.5rem;
    }}
    
    .subtitle {{
        color: #4A4A4A;
        font-size: 1.1em;
        line-height: 1.5;
        margin: 0.5rem 0;
        font-weight: 500;
    }}
    
    /* Hide default elements */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    
    /* Responsive adjustments */
    @media (max-width: 768px) {{
        .wheat-image-container {{
            width: 100px;
        }}
        .banner-content {{
            margin-left: 90px;
        }}
        .title-text h1 {{
            font-size: 1.8em;
        }}
        .title-text h2 {{
            font-size: 1.4em;
        }}
    }}
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
        <div class="wheat-image-container"></div>
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
                    
                    st.markdown('<div class="result-container">', unsafe_allow_html=True)
                    
                    if class_names[result_index] == "Healthy":
                        st.markdown(
                            f'<div class="disease-result disease-healthy">✨ Your wheat plant is healthy!</div>',
                            unsafe_allow_html=True
                        )
                        st.balloons()
                    else:
                        st.markdown(
                            f'<div class="disease-result disease-warning">⚠️ Disease Detected: {class_names[result_index]}</div>',
                            unsafe_allow_html=True
                        )
                    
                    st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.current_view == 'gallery':
        uploaded_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'])
        if uploaded_file:
            st.image(uploaded_file)
            if st.button("Analyze Image", key="analyze_upload"):
                with st.spinner("📊 Analyzing your wheat leaf..."):
                    st.snow()
                    result_index = model_prediction(uploaded_file)
                    class_names = ["Brown_rust", "Healthy", "Loose_Smut", "Yellow_rust", "septoria"]
                    
                    st.markdown('<div class="result-container">', unsafe_allow_html=True)
                    
                    if class_names[result_index] == "Healthy":
                        st.markdown(
                            f'<div class="disease-result disease-healthy">✨ Your wheat plant is healthy!</div>',
                            unsafe_allow_html=True
                        )
                        st.balloons()
                    else:
                        st.markdown(
                            f'<div class="disease-result disease-warning">⚠️ Disease Detected: {class_names[result_index]}</div>',
                            unsafe_allow_html=True
                        )
                    
                    st.markdown('</div>', unsafe_allow_html=True) 