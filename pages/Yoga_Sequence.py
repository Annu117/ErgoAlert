import streamlit as st
from PIL import Image
st.set_page_config(
    page_title="Real-time Risk Monitor",
    page_icon="E_logo1.png",
    layout="wide"
)
# Function to load and display images
def load_image(image_path):
    img = Image.open(image_path)
    st.image(img, caption='', use_column_width=True)
custom_css = """
            <style>
                .main {
                    margin-left: -70px;
                    padding: 20px;
                    margin-top:  -80px; 
                }
                .section-title {
                    font-size: 20px;
                    font-weight: bold;
                    margin-bottom: 20px;
                }
            </style>
        """
st.markdown(custom_css, unsafe_allow_html=True)
# Function to display yoga pose description
def yoga_pose(description, instructions, image_path):
    col1, col2 = st.columns([1, 2])  # Adjusted column width proportions
    with col1:
        st.image(image_path, use_column_width=True)
    with col2:
        st.markdown(f"<div class='section-title' ;> {description}</div>\n\n{instructions}", unsafe_allow_html=True)

# Main Streamlit app
def Yoga_Poses():
    st.subheader("Yoga Sequence for Desk Workers")
    st.write("If your work involves prolonged sitting, try these yoga poses to counteract stiffness and promote well-being. Remember Yoga Sutra 2.46: Sthira Sukha Asanam, which encourages finding steadiness and ease.")

    yoga_pose(
        "Hands and Knees with Wrist Stretch",
        "- Alleviates forearm and wrist tension.\n- Start on hands and knees, palms up, fingers back.\n- Rock gently or try Cat-Cow motions for 5–10 breaths.",
        "wrist_stretch.jpg"
    )
    yoga_pose(
        "Vasisthasana Variation (Modified Side Plank or Gate Pose)",
        "- Stretches side body, counteracting compression.\n- From Tabletop, extend one foot back, arm overhead.\n- Hold for 5–10 breaths on each side.",
        "virabhadrasana.jpg"
    )
    yoga_pose(
        "Adho Mukha Svanasana (Downward-Facing Dog)",
        "- Lengthens hamstrings, improves circulation.\n- Lift hips, spread fingers, and breathe for 5–10 breaths.",
        "adho-mukha-svanasana.jpg"
    )
    yoga_pose(
        "Anjaneyasana (Low Lunge with Locust Arms)",
        "- Counters hip flexion from sitting. \n- Step one foot forward, arms interlaced, lifting chest.\n- Hold for 5–10 breaths on each side.",
        "anjaney.jpg"
    )
    yoga_pose(
        "Ustrasana (Camel)",
        "- Counters sitting shape, promotes ease.\n- Stand on knees, hands on low back, lift chest.\n- Breathe for 5–10 cycles.",
        "ustrasana.jpg"

    )
    
Yoga_Poses()
# if __name__ == "__main__":
#     main()
