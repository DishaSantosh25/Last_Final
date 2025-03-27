import streamlit as st
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image

# Define your model architecture.
# Replace this with your actual model class and architecture.
class WheatModel(nn.Module):
    def __init__(self):
        super(WheatModel, self).__init__()
        self.conv1 = nn.Conv2d(3, 16, kernel_size=3, stride=1, padding=1)
        self.relu = nn.ReLU()
        self.pool = nn.MaxPool2d(2, 2)
        # Assuming input image size is 128x128, after pooling it becomes 64x64.
        # Adjust the linear layer size as per your architecture.
        self.fc1 = nn.Linear(16 * 64 * 64, 5)  # 5 classes

    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))
        x = x.view(x.size(0), -1)
        x = self.fc1(x)
        return x

# Load the PyTorch model from .pth file.
def load_model():
    model = WheatModel()
    # Load the state dict; adjust the path if needed.
    model.load_state_dict(torch.load("./wheat_disease_model.pth", map_location=torch.device("cpu")))
    model.eval()
    return model

# PyTorch Model Prediction Function
def model_prediction(test_image):
    model = load_model()
    # Open the image and convert to RGB
    image = Image.open(test_image).convert("RGB")
    
    # Define the image transformations
    transform = transforms.Compose([
        transforms.Resize((128, 128)),
        transforms.ToTensor(),
        # You can add normalization here if required by your model:
        # transforms.Normalize(mean=[...], std=[...])
    ])
    
    input_tensor = transform(image)
    input_tensor = input_tensor.unsqueeze(0)  # add batch dimension

    with torch.no_grad():
        outputs = model(input_tensor)
        prediction = torch.argmax(outputs, dim=1)
    
    return prediction.item()

st.header("Disease Recognition")

# Upload an image
test_image = st.file_uploader("Choose an Image:")

if test_image is not None:
    # Option to display the uploaded image
    if st.button("Show Image"):
        st.image(test_image, use_column_width=True)

    # Predict the disease
    if st.button("Predict"):
        st.snow()  # decorative effect
        st.write("Our Prediction")
        result_index = model_prediction(test_image)
        # Define class names corresponding to model output indices
        class_name = ["Brown_rust", "Healthy", "Loose_Smut", "Yellow_rust", "septoria"]
        st.success("Model is Predicting it's a {}".format(class_name[result_index]))
else:
    st.info("Please upload an image to begin.")
