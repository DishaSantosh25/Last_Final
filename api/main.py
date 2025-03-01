import streamlit as st

def main():
    # Configure page
    st.set_page_config(page_title="Wheat Leaf Identifier", layout="centered")

    # Initialize session state for button clicks
    if "take_picture_clicked" not in st.session_state:
        st.session_state.take_picture_clicked = False
    if "import_picture_clicked" not in st.session_state:
        st.session_state.import_picture_clicked = False

    # Custom CSS for layout & styling
    st.markdown(
        """
        <style>
        /* Hide default Streamlit hamburger menu & footer */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        /* Page background color */
        [data-testid="stAppViewContainer"] {
            background-color: #FFFFFF;
        }

        /* Top bar */
        .top-bar {
            display: flex; 
            align-items: center; 
            padding: 1rem 0; 
            margin-left: 16px;
        }
        .top-bar-icon {
            color: black; 
            font-size: 20px; 
            margin-right: 4px; 
            cursor: pointer;
        }
        .top-bar-text {
            color: rgba(0,0,0,0.7); 
            font-size: 16px; 
            font-family: Roboto;
            cursor: pointer;
        }

        /* Header container */
        .header-container {
            position: relative; 
            height: 200px; 
            background-color: #E5C07B; 
            border-radius: 24px; 
            margin: 16px; 
            overflow: hidden;
        }
        .header-text {
            position: absolute; 
            left: 24px; 
            top: 50px;
            color: white; 
            font-family: Roboto;
        }
        .header-title {
            font-size: 32px; 
            font-weight: bold; 
            margin: 0;
        }
        .header-subtitle {
            font-size: 24px; 
            margin: 4px 0 0 0;
        }
        .header-image {
            position: absolute; 
            right: -20px; 
            top: 0; 
            bottom: 0; 
            width: 200px;
        }

        /* Centered section */
        .center-section {
            text-align: center; 
            margin-top: 5px;
        }
        .center-section p {
            font-size: 16px; 
            color: rgba(0,0,0,0.7); 
            line-height: 1.5; 
            font-family: Roboto;
        }

        /* Button container */
        .button-container {
            margin: 16px;
        }
        .custom-button {
            width: 100%; 
            padding: 16px 20px; 
            background-color: #98C379; 
            border: none; 
            border-radius: 16px; 
            cursor: pointer; 
            margin-bottom: 16px;
            display: flex; 
            justify-content: space-between; 
            align-items: center;
        }
        .button-texts {
            display: flex; 
            flex-direction: column;
        }
        .button-title {
            color: white; 
            font-size: 18px; 
            font-weight: 600; 
            font-family: Roboto; 
            margin: 0;
        }
        .button-subtitle {
            color: rgba(255,255,255,0.8); 
            font-size: 14px; 
            font-family: Roboto; 
            margin: 0;
        }
        .button-icon {
            color: white; 
            font-size: 24px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Top bar with back button
    st.markdown(
        """
        <div class="top-bar">
            <span class="top-bar-icon">&#8592;</span>
            <span class="top-bar-text">back</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Header with wheat background
    st.markdown(
        """
        <div class="header-container">
            <div class="header-text">
                <h1 class="header-title">Wheat Leaf</h1>
                <h2 class="header-subtitle">Identifier</h2>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Logo & tagline
    col1, col2, col3 = st.columns([3, 1, 3])
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

    # Buttons
    st.markdown('<div class="button-container">', unsafe_allow_html=True)

    # 1) Take picture button (Click triggers camera input)
    if st.button("📷 Take Picture of Your Plant"):
        st.session_state.take_picture_clicked = True
        st.session_state.import_picture_clicked = False  # Reset gallery click

    if st.session_state.take_picture_clicked:
        pic_file = st.camera_input("Capture an image")
        if pic_file is not None:
            st.image(pic_file, caption="Captured Image")

    # 2) Import from gallery button (Click triggers file uploader)
    if st.button("🖼 Import from Gallery"):
        st.session_state.import_picture_clicked = True
        st.session_state.take_picture_clicked = False  # Reset camera click

    if st.session_state.import_picture_clicked:
        uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
        if uploaded_file is not None:
            st.image(uploaded_file, caption="Uploaded Image")

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
