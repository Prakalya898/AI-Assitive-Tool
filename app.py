import streamlit as st
from streamlit_lottie import st_lottie
from tool import ITT
from ttstool import GoogleTransDeep
import os
import time
from pathlib import Path
import json

# Set API Key
os.environ["GOOGLE_API_KEY"] = "AIzaSyBZtlNTr1ZN35BLcMGJgrC3e248r8HWZPY"  # Replace this

# Helper to load lottie files
def load_lottiefile(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

# Page config
st.set_page_config(page_title="🤖AI Assistive Tool", layout="wide")

# Load animations
assistive_lottie = load_lottiefile("animations/assistive_ai.json")
loading_lottie = load_lottiefile("animations/loading.json")

# Ensure output folder exists
os.makedirs("output", exist_ok=True)

# Session state setup
if "page" not in st.session_state:
    st.session_state.page = "main"
if "trigger_processing" not in st.session_state:
    st.session_state.trigger_processing = False

# -------------- PAGE: MAIN -------------------
if st.session_state.page == "main":
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col3:
        st_lottie(assistive_lottie, height=220)

    st.markdown("<h1 style='text-align: center;'>🤖 AI Assistive Tool</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Designed to help blind and autistic users understand image content using voice and translation.</p>", unsafe_allow_html=True)

    uploaded_image = st.file_uploader("📸 Upload an image", type=["png", "jpg", "jpeg"])
    input_text = st.text_input("💭 Your Question", placeholder="Ask about the image (e.g., 'What is the nutritional value?')")

    if st.button("🚀 Process"):
        if not uploaded_image:
            st.error("Please upload an image.")
        elif not input_text:
            st.error("Please enter your query.")
        else:
            st.session_state.uploaded_image = uploaded_image
            st.session_state.input_text = input_text
            st.session_state.page = "loading"
            st.session_state.trigger_processing = True  # This makes sure loading page runs only on click
            st.rerun()

# -------------- PAGE: LOADING -------------------
elif st.session_state.page == "loading":
    if st.session_state.trigger_processing:
        st.markdown(
            """
            <div style="display: flex; justify-content: center; align-items: center; height: 100vh;
                        background-color: rgba(0, 0, 0, 0.8); z-index: 999;">
                <div>
            """,
            unsafe_allow_html=True
        )

        st_lottie(loading_lottie, height=300)
        st.markdown("<h3 style='text-align: center; color: white;'>Please wait, processing your request...</h3>", unsafe_allow_html=True)

        st.markdown("</div></div>", unsafe_allow_html=True)

        # Wait before actual processing
        time.sleep(3)
        st.session_state.page = "result"
        st.session_state.trigger_processing = False
        st.rerun()
    else:
        st.session_state.page = "main"
        st.rerun()

# -------------- PAGE: RESULT -------------------
elif st.session_state.page == "result":
    uploaded_image = st.session_state.uploaded_image
    input_text = st.session_state.input_text

    try:
        image_bytes = uploaded_image.read()
        image_name = os.path.splitext(uploaded_image.name)[0]
        audio_filename = f"output/{image_name}_ta.mp3"

        USE_FAKE_RESULT = False  # Toggle to False for live image-to-text

        # STEP 1: Show the text result
        if USE_FAKE_RESULT:
            result = (
                "To withdraw money, press the ‘Get Cash’ button. It is the second button from the left on the top row, and it is blue in color. "
                "Then, choose the amount you want. After that, press Yes to confirm. The cash will come out from the slot below. "
                "Don’t forget to take your card and receipt."
            )
        else:
            image_to_text_tool = ITT(image_bytes=image_bytes)
            result = image_to_text_tool.invoke({"query": input_text})

        st.subheader("🧠 Image Caption / Agent Output:")
        st.write(result)

        # STEP 2: Display loading animation while translating
        audio_loading = load_lottiefile("animations/audio_loading.json")
        col_left, col_center, col_right = st.columns([1, 2, 1])
        with col_center:
            loading_placeholder = st.empty()
            with loading_placeholder.container():
                st_lottie(audio_loading, height=200, key="audio_loading")
                st.markdown("<p style='text-align: center;'>🔊 Translating and generating audio......</p>", unsafe_allow_html=True)

        # STEP 3: Perform translation and TTS
        translator = GoogleTransDeep()
        response = translator.run(query=result, output_audio_filename=audio_filename)

        # STEP 4: Remove animation and show result
        loading_placeholder.empty()

        if "error" in response:
            st.error(response["error"])
        else:
            st.subheader("🌐 Translated Output (Tamil):")
            st.write(response["translated_text"])

            with open(response["audio_path"], "rb") as f:
                st.audio(f.read(), format="audio/mp3")

        st.session_state.page = "main"

    except Exception as e:
        st.error(f"Error during processing: {e}")
        st.session_state.page = "main"
