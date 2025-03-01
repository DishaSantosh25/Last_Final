import streamlit as st
import tensorflow as tf
import numpy as np

# TensorFlow Model Prediction Function
def model_prediction(test_image):
    model = tf.keras.models.load_model("./wheat.h5")
    image = tf.keras.preprocessing.image.load_img(test_image, target_size=(128, 128))
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr])  # convert single image to batch format
    predictions = model.predict(input_arr)
    return np.argmax(predictions)  # return index of highest prediction

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

