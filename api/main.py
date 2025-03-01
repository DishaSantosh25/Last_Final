import streamlit as st

def main():
    # Configure page
    st.set_page_config(page_title="Wheat Leaf Identifier", layout="centered")

    # Inject custom CSS for layout & styling
    st.markdown(
        """
        <style>
        /* Hide default Streamlit components */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .st-emotion-cache-1dp5vir {display: none;}

        /* Custom button hover effects */
        .custom-button:hover {
            opacity: 0.9;
            transform: scale(1.02);
            transition: all 0.3s ease;
        }

        /* Hide actual file uploader inputs */
        .stFileUploader {
            display: none !important;
        }

        /* Adjust camera input styling */
        [data-testid="stCameraInputButton"] {
            display: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Rest of your existing CSS styles here...
    # Keep all your existing CSS styles as they were

    # Header with wheat background & image (keep existing code)
    # ...

    # Logo & tagline (keep existing code)
    # ...

    # Modified Action buttons section
    st.markdown('<div class="button-container">', unsafe_allow_html=True)

    # 1) "Take picture" button
    with st.container():
        st.markdown(
            """
            <label class="custom-button" for="camera-input">
                <div class="button-texts">
                    <p class="button-title">Take picture</p>
                    <p class="button-subtitle">of your plant</p>
                </div>
                <span class="button-icon">&#128247;</span>
            </label>
            """,
            unsafe_allow_html=True
        )
        pic_file = st.camera_input("", key="camera-input")
        if pic_file:
            st.image(pic_file, caption="Captured Image")

    # 2) "Import from gallery" button
    with st.container():
        st.markdown(
            """
            <label class="custom-button" for="gallery-input">
                <div class="button-texts">
                    <p class="button-title">Import</p>
                    <p class="button-subtitle">from your gallery</p>
                </div>
                <span class="button-icon">&#128247;</span>
            </label>
            """,
            unsafe_allow_html=True
        )
        uploaded_file = st.file_uploader("", type=["png","jpg","jpeg"], key="gallery-input")
        if uploaded_file:
            st.image(uploaded_file, caption="Uploaded Image")

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()