import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Real-time Risk Monitor",
    page_icon="E_logo1.png",
    layout="wide"
)
# Custom CSS to reduce header space
custom_css = """
    <style>
        # .stApp {
        #     margin-top: -80px;
            
        # }
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f5f5f5;
        }
        .main {
            margin-left: -200px; /* Width of the sidebar */
            padding: 20px;
            margin-top:  -100px; 

            background-color: #ffffff;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            .guidelines-container,
            .remember-container {
                margin-top: 20px;
                background-color: #f9f9f9;
                padding: 15px;
                border-radius: 8px;
        }
        }
    </style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

def general_guidline():
    st.subheader("Sitting Posture Guidelines")
    # st.markdown("To promote safety and comfort during work")
    col1, col2 = st.columns(2)
    with col1:
        G_posture_image = Image.open("sitting_pose.png")
        st.image(G_posture_image, caption="Good Sitting Posture", use_column_width=True)
    with col2:
        st.write("")
        st.write("")
        B_posture_image = Image.open("W_sitting_pose.png")
        st.image(B_posture_image, caption="Bad Sitting Posture", use_column_width=True)
    # Load and display the image
    # posture_image = Image.open("Ergo_Check1.png")
    # st.image(posture_image, caption="Sitting Posture", use_column_width=True)
    st.markdown("---")
    st.subheader("Position for Safety and Comfort")
    guidelines = [
        "HEAD level in line with the torso",
        "FOREARMS, WRISTS, and HANDS relaxed and straight",
        "ELBOWS close to the body, bent between 90° and 120°",
        "EARS in line with shoulders",
        "SHOULDERS back and relaxed, not rounded or elevated",
        "BACK straight and supported, sitting upright or leaning back slightly",
        "THIGHS and HIPS supported by a well-padded seat, parallel to the floor",
        "FEET forward, fully supported by the floor or footrest"
    ]
    for guideline in guidelines:
        st.markdown(f" - {guideline}")

    st.subheader("Remember")
    remember_points = [
        "WHEN KEYING, float your hands over the keyboard, and use palm rests between bursts of keying.",
        "WHEN MOUSING, keep your wrists straight, and use the elbow to pivot.",
        "ADJUST your chair to fit you, if possible.",
        "CHANGE your working position often throughout the day, stretching your fingers, hands, arms, and torso, and by standing and walking around for a few minutes periodically."
    ]
    for point in remember_points:
        st.markdown(f" - {point}")
    st.markdown("---")

   
general_guidline()
