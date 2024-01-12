import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Real-time Risk Monitor",
    page_icon="E_logo1.png",
    layout="wide"
)
st.markdown('<link rel="stylesheet" type="text/css" href="styles.css">', unsafe_allow_html=True)

def home():
    custom_css = """
            <style>
                .main {
                    margin-left: -70px;
                    padding: 20px;
                    margin-top:  -110px; 
                }
                .section-title {
                    font-size: 24px;
                    font-weight: bold;
                    margin-bottom: 20px;
                }
            </style>
        """
    st.markdown(custom_css, unsafe_allow_html=True)
    # Page title and description
    st.header("Ergonomic Risk Analysis")
    st.write(
        "Welcome to the Ergonomic Risk Analysis Website, a real-time solution for assessing and mitigating ergonomic risks during work. "
        "Utilizing computer vision and the RULA scoring method, this system provides actionable insights and alerts to enhance workplace safety."
    )
    st.markdown(
    f"""
    <style>
        .small-image {{
            width: 20%;  /* Adjust the width percentage as needed */
        }}
    </style>
    """,
    unsafe_allow_html=True
    )
    page_width = 5000
    # Image or illustration
    st.image("image (2).png", use_column_width=True, caption="Ergonomic Workspace")

    # Features and Benefits section
    st.markdown("<div class='section-title'>Key Features</div>", unsafe_allow_html=True)
    st.write(
        "- **Real-time Ergonomic Analysis:** Continuously monitor and analyze users' postures in real-time using computer vision.\n"
        "- **Ergonomic Suggestions:** Receive personalized ergonomic advice based on RULA scores, promoting better posture and reducing risks.\n"
        "- **Alert System:** Instant notifications for supervisors or workers when extended periods of harmful postures are detected.\n"
        # "- **Data Insights:** Access comprehensive data insights to identify trends and areas for improvement.\n"
        # "- **User-Friendly Interface:** Easy-to-use interface for a seamless experience."
    )

    # Get Started Section
    st.markdown("<div class='section-title'>Get Started</div>", unsafe_allow_html=True)
    st.write(
        "To begin using the Ergonomic Risk Analysis System, follow these steps:\n"
        "1. **Start Analysis:** Click the 'Start Analysis' button to initiate real-time posture monitoring.\n"
        "2. **Receive Scores:** Get RULA scores along with ergonomic suggestions displayed in the interface.\n"
        "3. **Alerts and Recommendations:** Receive alerts for prolonged harmful postures and follow ergonomic recommendations.\n"
        "4. **Enhance Workplace Safety:** Implement suggested changes to improve the overall ergonomic environment."
    )

    # Contact Us Section
    st.markdown("<div class='section-title'>Contact Us</div>", unsafe_allow_html=True)
    st.write(
        "For any questions, feedback, or support, feel free to contact us at [contact@ergoalert.com](mailto:contact@ergoalert.com).\n"
        "We value your input and are here to assist you in creating a safer and more ergonomic workplace."
    )

    # Footer
    st.markdown(
        """
        *Built with ❤️ by ErgoAlert
        """
    )

home()
