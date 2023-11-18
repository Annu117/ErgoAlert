import streamlit as st
st.set_page_config(
    page_title="Real-time Risk Monitor",
    page_icon="E_logo1.png",
    layout="wide"
)
custom_css = """
        <style>
            .main {
                margin-left: -80px;
                padding: 20px;
                margin-top:  -110px; 
            }
            body {
                font-family: 'Arial', sans-serif;
                background-color: #f5f5f5;
            }
            .section-title {
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 20px;
            }
        </style>
    """
st.markdown(custom_css, unsafe_allow_html=True)
def display_guidelines():
    st.header("Ergonomic Posture Alert")

    rula_score = st.slider(
        "Select your RULA score (1 - Low Risk, 2 - Moderate, 3 - High, 4 - Very High)",
        1, 4, 1, 1
    )
    if rula_score == 1:
        st.markdown("<div class='section-title' ;>Congratulations! You are at low risk.</div>", unsafe_allow_html=True)

        st.markdown(
            # "## Congratulations! You are at **low risk.**"
            "\n\nMaintain your current posture; it's ergonomic and safe."
            "\n\nRemember to take short breaks for stretching and movement every 30 minutes."
        )
    elif rula_score == 2:
        st.markdown("<div class='section-title'>You can improve your posture for better comfort and well-being.</div>", unsafe_allow_html=True)
        st.markdown(
            "\n\n- Adjust your chair and desk heights for better support."
            "\n\n- Consider using ergonomic accessories like lumbar support or a footrest."
            "\n\n- Take regular breaks every 30 minutes for stretching and changing positions."
        )
    elif rula_score == 3:
        st.markdown("<div class='section-title'>High ergonomic risk detected!</div>", unsafe_allow_html=True)
        st.markdown(
            "\n\n- **Address Visible Ergonomic Issues:** Identify and rectify any visible ergonomic issues with your chair, desk, or computer setup."
            "\n\n- **Perform Exercises and Stretches:** Incorporate exercises and stretches into your routine to relieve tension and improve your posture. Focus on neck, shoulder, and back stretches."
            "\n\n- **Take More Frequent Breaks:** Increase the frequency of breaks throughout your work session. Use breaks to stand, stretch, and change your posture."
            "\n\n- **Consult with an Ergonomic Professional:** Consider consulting with an ergonomic professional for personalized advice. They can provide specific recommendations based on your workspace and habits."
        )
    elif rula_score == 4:
        st.markdown("<div class='section-title'>Immediate intervention required!</div>", unsafe_allow_html=True)
        st.markdown(
            "\n\n- **Professional Ergonomic Assessment:** Consider a professional ergonomic assessment to identify and rectify specific issues. A professional can provide tailored solutions based on your unique needs."
            "\n\n- **Use Alternative Workstations:** Explore alternative workstations such as standing desks, if possible. Alternate between sitting and standing to reduce prolonged sitting."
            "\n\n- **Prioritize Comfort and Well-being:** Prioritize your comfort and well-being over extended work sessions. Take regular breaks, stretch, and listen to your body."
            "\n\n- **Seek Medical Advice if Necessary:** If discomfort persists, consider seeking medical advice for a more thorough evaluation."
        )
display_guidelines()
