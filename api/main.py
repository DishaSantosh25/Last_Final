import streamlit as st

def main():
    # Configure page (keep original config)
    st.set_page_config(page_title="Wheat Leaf Identifier", layout="centered")

    # Inject custom CSS (keep original styling)
    st.markdown(
        """
        <style>
        /* Your original CSS here - unchanged */
        /* Add just these 3 new rules at the end */
        .stFileUploader { display: none; }
        [data-testid="stCameraInputButton"] { display: none; }
        .clickable-label { cursor: pointer; }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Keep all your original header code exactly as it was
    # Header with wheat background & image
    st.markdown(
        """
        <div class="header-container">
            <div class="header-text">
                <h1 class="header-title">Wheat Leaf</h1>
                <h2 class="header-subtitle">Identifier</h2>
            </div>
            <img src="https://raw.githubusercontent.com/yourrepo/wheat.webp" class="header-image"/>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Keep original logo & tagline code exactly as it was
    col1, col2, col3 = st.columns([3,1,3])
    with col2:
        st.image("https://raw.githubusercontent.com/yourrepo/logo.png", width=70)

    st.markdown(
        """
        <div class="center-section">
            <p>Supporting Farmers in<br>Safeguarding their Crop Health</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Keep original spacing
    st.write("")
    st.write("")
    st.write("")

    # Modified button section only
    st.markdown('<div class="button-container">', unsafe_allow_html=True)

    # 1) Take Picture Button
    with st.container():
        # Camera input linked to label
        pic_file = st.camera_input("", key="camera_input")
        st.markdown(
            """
            <label class="clickable-label" for="camera_input">
                <div class="custom-button">
                    <div class="button-texts">
                        <p class="button-title">Take picture</p>
                        <p class="button-subtitle">of your plant</p>
                    </div>
                    <span class="button-icon">&#128247;</span>
                </div>
            </label>
            """,
            unsafe_allow_html=True
        )
        if pic_file:
            st.image(pic_file, caption="Captured Image")

    # 2) Import Button
    with st.container():
        # File uploader linked to label
        uploaded_file = st.file_uploader("", type=["png","jpg","jpeg"], key="gallery_input")
        st.markdown(
            """
            <label class="clickable-label" for="gallery_input">
                <div class="custom-button">
                    <div class="button-texts">
                        <p class="button-title">Import</p>
                        <p class="button-subtitle">from your gallery</p>
                    </div>
                    <span class="button-icon">&#128247;</span>
                </div>
            </label>
            """,
            unsafe_allow_html=True
        )
        if uploaded_file:
            st.image(uploaded_file, caption="Uploaded Image")

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()