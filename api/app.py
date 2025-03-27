import streamlit as st
import torch
import numpy as np
from PIL import Image
import torchvision.transforms as transforms
import base64

# Page configuration
st.set_page_config(
    page_title="Wheat Leaf Identifier",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Load PyTorch model
@st.cache_resource
def load_model():
    model = torch.load("./wheat_disease_model.pth", map_location=torch.device('cpu'))
    model.eval()
    return model

def model_prediction(image_data):
    model = load_model()
    transform = transforms.Compose([
        transforms.Resize((128, 128)),
        transforms.ToTensor()
    ])
    image = Image.open(image_data).convert("RGB")
    image = transform(image).unsqueeze(0)  # Add batch dimension
    output = model(image)
    return torch.argmax(output, dim=1).item()

# UI Layout
st.title("🌾 Wheat Leaf Identifier")
st.write("Upload an image of a wheat leaf to detect any potential disease.")

uploaded_file = st.file_uploader("Choose a wheat leaf image...", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)
    if st.button("Analyze Image"):
        with st.spinner("Analyzing the image..."):
            result_index = model_prediction(uploaded_file)
            class_names = ["Brown_rust", "Healthy", "Loose_Smut", "Yellow_rust", "Septoria"]
            disease_name = class_names[result_index]
            
            st.subheader("Prediction Result")
            if disease_name == "Healthy":
                st.success("✅ Your wheat plant is healthy!")
            else:
                st.error(f"⚠️ Disease Detected: {disease_name}")
                recommendations = {
                    "Brown_rust": "Apply fungicide treatment immediately and monitor other plants.",
                    "Loose_Smut": "Remove infected plants and use disease-resistant varieties.",
                    "Yellow_rust": "Apply fungicides and improve air circulation.",
                    "Septoria": "Use foliar fungicides and maintain proper spacing between plants."
                }
                st.info(recommendations.get(disease_name, "Seek expert guidance for treatment."))
