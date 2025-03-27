import streamlit as st
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image
import base64
import numpy as np

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Wheat Leaf Identifier",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# -------------------------------
# Helper: Load and Encode Wheat Image
# -------------------------------
def get_wheat_image():
    try:
        with open("extracted_wheat.png", "rb") as f:
            data = f.read()
            encoded = base64.b64encode(data).decode()
            return f"data:image/png;base64,{encoded}"
    except Exception as e:
        print(f"Error loading wheat image: {e}")
        try:
            with open("wheat.jpg", "rb") as f:
                data = f.read()
                encoded = base64.b64encode(data).decode()
                return f"data:image/jpeg;base64,{encoded}"
        except Exception as e:
            print(f"Error loading fallback image: {e}")
            return None

wheat_image = get_wheat_image()

# -------------------------------
# Custom CSS with Dynamic Wheat Image
# -------------------------------
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
        padding: 2.8rem 1.2rem;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: visible;
        min-height: 180px;
        display: flex;
        align-items: center;
        justify-content: flex-start;
        box-shadow: 0 4px 15px rgba(245, 192, 107, 0.2);
    }}
    /* Banner Content */
    .banner-content {{
        position: relative;
        z-index: 2;
        flex: none;
        width: 52%;
        padding: 0.8rem 0.5rem 0.8rem 1.2rem;
        display: flex;
        flex-direction: column;
        justify-content: center;
        min-width: 220px;
    }}
    /* Title Container */
    .title-container {{
        display: flex;
        flex-direction: column;
        gap: 10px;
        width: 100%;
        padding: 0.7rem 0;
    }}
    .title-text {{
        color: #FFFFFF;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
        line-height: 1.2;
    }}
    .title-text h1 {{
        font-size: 2.3em;
        font-weight: 800;
        margin: 0;
    }}
    .title-text h2 {{
        font-size: 1.8em;
        font-weight: 600;
        margin: 0;
        opacity: 0.95;
    }}
    /* Wheat Image Container */
    .wheat-image-wrapper {{
        position: absolute;
        right: -15px;
        top: 50%;
        transform: translateY(-50%);
        height: 100%;
        width: 48%;
        display: flex;
        align-items: center;
        justify-content: flex-end;
    }}
    .wheat-image {{
        position: absolute;
        right: 0;
        height: 180%;
        width: 220px;
        background-image: url('{wheat_image if wheat_image else ""}');
        background-size: contain;
        background-position: center right;
        background-repeat: no-repeat;
        transform-origin: center;
        transform: translateY(0) scale(1.15);
        filter: contrast(1.05) brightness(1.02);
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
        font-weight: 600;
        font-size: 1.3em;
        text-align: center;
        transition: all 0.3s ease;
    }}
    .disease-warning {{
        background: linear-gradient(135deg, #FFE4E4 0%, #FFD0D0 100%);
        color: #D43B3B;
        border: 1px solid rgba(212, 59, 59, 0.3);
        box-shadow: 0 2px 12px rgba(212, 59, 59, 0.15);
        animation: pulseWarning 2s infinite;
    }}
    .disease-healthy {{
        background: linear-gradient(135deg, #E6FFE6 0%, #98FB98 100%);
        color: #228B22;
        border: 1px solid rgba(34, 139, 34, 0.3);
        box-shadow: 0 2px 12px rgba(34, 139, 34, 0.15);
    }}
    @keyframes pulseWarning {{
        0% {{ transform: scale(1); box-shadow: 0 2px 12px rgba(212, 59, 59, 0.15); }}
        50% {{ transform: scale(1.02); box-shadow: 0 4px 16px rgba(212, 59, 59, 0.25); }}
        100% {{ transform: scale(1); box-shadow: 0 2px 12px rgba(212, 59, 59, 0.15); }}
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
        margin: 0.5rem 0 2.5rem 0;
        font-weight: 500;
    }}
    /* Hide default elements */
    #MainMenu, footer {{ visibility: hidden; }}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Model Architecture (Simple CNN)
# -------------------------------
class WheatDiseaseModel(nn.Module):
    def __init__(self, num_classes=5):
        super(WheatDiseaseModel, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=3, stride=1, padding=1),  # expects keys "conv.0.weight", etc.
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2)
        )
        # Assuming input images are resized to 128x128, after two pooling layers we have 32x32 spatial dims
        self.fc = nn.Sequential(
            nn.Linear(32 * 32 * 32, 128),
            nn.ReLU(),
            nn.Linear(128, num_classes)
        )

    def forward(self, x):
        x = self.conv(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return x

# -------------------------------
# Model Loading and Prediction Functions
# -------------------------------
@st.cache_resource
def load_model():
    # Instantiate the model architecture
    model = WheatDiseaseModel(num_classes=5)
    # Load the state dictionary (ensure the path is correct)
    state_dict = torch.load("./wheat_disease_model.pth", map_location=torch.device("cpu"))
    model.load_state_dict(state_dict)
    model.eval()
    return model

def model_prediction(image_data):
    model = load_model()
    # Open the image and convert to RGB
    image = Image.open(image_data).convert("RGB")
    # Use transforms similar to training (adjust size if needed)
    transform = transforms.Compose([
        transforms.Resize((128, 128)),
        transforms.ToTensor(),
        # Use normalization parameters matching training if available
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])
    input_tensor = transform(image).unsqueeze(0)
    with torch.no_grad():
        output = model(input_tensor)
        predicted_class = output.argmax(dim=1).item()
    return predicted_class

# -------------------------------
# UI Elements
# -------------------------------

# Header Banner with Wheat Image
st.markdown("""
    <div class="header-banner">
        <div class="banner-content">
            <div class="title-container">
                <div class="title-text">
                    <h1>Wheat Leaf</h1>
                    <h2>Identifier</h2>
                </div>
            </div>
        </div>
        <div class="wheat-image-wrapper">
            <div class="wheat-image" role="img" aria-label="Decorative wheat image"></div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Center Section
st.markdown("""
    <div class="center-section">
        <div class="leaf-icon">🌿</div>
        <div class="subtitle">
            Supporting Farmers in<br>Safeguarding their Crop Health
        </div>
    </div>
""", unsafe_allow_html=True)

# Session state for view control
if 'current_view' not in st.session_state:
    st.session_state.current_view = None

# Layout: Create columns for better design
col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    camera_btn = st.button("📸 Take picture of your plant")
    gallery_btn = st.button("🖼️ Import from your gallery")
    if camera_btn:
        st.session_state.current_view = 'camera'
    if gallery_btn:
        st.session_state.current_view = 'gallery'

    # Camera view
    if st.session_state.current_view == 'camera':
        camera_input = st.camera_input("")
        if camera_input:
            st.image(camera_input)
            if st.button("Analyze Image", key="analyze_camera"):
                with st.spinner("📊 Analyzing your wheat leaf..."):
                    result_index = model_prediction(camera_input)
                    class_names = ["Brown_rust", "Healthy", "Loose_Smut", "Yellow_rust", "septoria"]
                    st.markdown('<div class="result-container">', unsafe_allow_html=True)
                    if class_names[result_index] == "Healthy":
                        st.markdown(
                            f'<div class="disease-result disease-healthy">✨ Your wheat plant is healthy!</div>',
                            unsafe_allow_html=True
                        )
                    else:
                        disease_name = class_names[result_index]
                        recommendations = {
                            "Brown_rust": "Apply fungicide treatment immediately. Monitor other plants for early signs of infection.",
                            "Loose_Smut": "Remove and destroy infected plants. Consider using disease-resistant wheat varieties for future planting.",
                            "Yellow_rust": "Apply appropriate fungicides. Improve air circulation between plants and reduce humidity.",
                            "septoria": "Use foliar fungicides. Maintain proper spacing between plants to reduce moisture."
                        }
                        st.markdown(
                            f'''
                            <div class="disease-result disease-warning">⚠️ Disease Detected: {disease_name}</div>
                            <div class="disease-details">
                                <h3>About {disease_name}</h3>
                                <p>{recommendations.get(disease_name, "This wheat disease requires immediate attention. Early detection allows for effective treatment and prevents spread to other plants.")}</p>
                            </div>
                            ''',
                            unsafe_allow_html=True
                        )
                    st.markdown('</div>', unsafe_allow_html=True)

    # Gallery view
    elif st.session_state.current_view == 'gallery':
        uploaded_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'])
        if uploaded_file:
            st.image(uploaded_file)
            if st.button("Analyze Image", key="analyze_upload"):
                with st.spinner("📊 Analyzing your wheat leaf..."):
                    result_index = model_prediction(uploaded_file)
                    class_names = ["Brown_rust", "Healthy", "Loose_Smut", "Yellow_rust", "septoria"]
                    st.markdown('<div class="result-container">', unsafe_allow_html=True)
                    if class_names[result_index] == "Healthy":
                        st.markdown(
                            f'<div class="disease-result disease-healthy">✨ Your wheat plant is healthy!</div>',
                            unsafe_allow_html=True
                        )
                    else:
                        disease_name = class_names[result_index]
                        recommendations = {
                            "Brown_rust": "Apply fungicide treatment immediately. Monitor other plants for early signs of infection.",
                            "Loose_Smut": "Remove and destroy infected plants. Consider using disease-resistant wheat varieties for future planting.",
                            "Yellow_rust": "Apply appropriate fungicides. Improve air circulation between plants and reduce humidity.",
                            "septoria": "Use foliar fungicides. Maintain proper spacing between plants to reduce moisture."
                        }
                        st.markdown(
                            f'''
                            <div class="disease-result disease-warning">⚠️ Disease Detected: {disease_name}</div>
                            <div class="disease-details">
                                <h3>About {disease_name}</h3>
                                <p>{recommendations.get(disease_name, "This wheat disease requires immediate attention. Early detection allows for effective treatment and prevents spread to other plants.")}</p>
                            </div>
                            ''',
                            unsafe_allow_html=True
                        )
                    st.markdown('</div>', unsafe_allow_html=True)
