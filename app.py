import streamlit as st
import cv2
import numpy as np
import torch
import matplotlib.pyplot as plt
import copy
from utils import model
from utils import util
from utils.pose import pose_detector
import os
import pygame
import time
# Set Streamlit page configuration
st.set_page_config(
    page_title="ErgoAlert",
    # page_icon=":computer:",
    page_icon="ErgoAlert-logos_transparent.png",
    layout="wide"
)
css = """
    .section-title {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    """
custom_css = """
        <style>
            .main {
                margin-left: -70px;
                padding: 20px;
                margin-top:  -110px; 
            }
        </style>
    """
st.markdown(custom_css, unsafe_allow_html=True)

st.markdown('<link rel="stylesheet" type="text/css" href="styles.css">', unsafe_allow_html=True)
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
def load_page(pages):
    # Dynamically import the selected page
    page_module = __import__(f"pages.{pages[:-3]}", fromlist=["main"])
    page_module.main()
def home():
    # Page title and description
    # st.title("Ergonomic Risk Analysis System")
    # st.markdown("<div class='section-title'>Ergonomic Risk Analysis System</div>", unsafe_allow_html=True)
    st.header("Ergonomic Risk Analysis System")
    st.write(
        "Welcome to the Ergonomic Risk Analysis System, a real-time solution for assessing and mitigating ergonomic risks during work. "
        "Utilizing computer vision and the RULA scoring method, this system provides actionable insights and alerts to enhance workplace safety."
    )

    # Image or illustration
    st.image("image (2).png", use_column_width=True, caption="Ergonomic Workspace")

    # Features and Benefits section
    # st.header("Key Features and Benefits")
    st.markdown("<div class='section-title'>Key Features and Benefits</div>", unsafe_allow_html=True)
    st.write(
        "- **Real-time Ergonomic Analysis:** Continuously monitor and analyze users' postures in real-time using computer vision.\n"
        "- **Ergonomic Suggestions:** Receive personalized ergonomic advice based on RULA scores, promoting better posture and reducing risks.\n"
        "- **Alert System:** Instant notifications for supervisors or workers when extended periods of harmful postures are detected.\n"
        # "- **Data Insights:** Access comprehensive data insights to identify trends and areas for improvement.\n"
        # "- **User-Friendly Interface:** Easy-to-use interface for a seamless experience."
    )

    # Get Started Section
    # st.header("Get Started")
    st.markdown("<div class='section-title'>Get Started</div>", unsafe_allow_html=True)
    st.write(
        "To begin using the Ergonomic Risk Analysis System, follow these steps:\n"
        "1. **Start Analysis:** Click the 'Start Analysis' button to initiate real-time posture monitoring.\n"
        "2. **Receive Scores:** Get RULA scores along with ergonomic suggestions displayed in the interface.\n"
        "3. **Alerts and Recommendations:** Receive alerts for prolonged harmful postures and follow ergonomic recommendations.\n"
        "4. **Enhance Workplace Safety:** Implement suggested changes to improve the overall ergonomic environment."
    )

    # Contact Us Section
    # st.header("Contact Us")
    st.markdown("<div class='section-title'>Contact Us</div>", unsafe_allow_html=True)

    st.write(
        "For any questions, feedback, or support, feel free to contact us at [contact@ergoguard.com](mailto:contact@ergoguard.com).\n"
        "We value your input and are here to assist you in creating a safer and more ergonomic workplace."
    )

    # Footer
    st.markdown(
        """
        *Built with ❤️ by ErgoAlert
        """
    )
def RealTimeMonitor():
    st.markdown('<link rel="stylesheet" type="text/css" href="styles.css">', unsafe_allow_html=True)

    # Initialize the model and pose detector
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model_rula = model.NN_base().to(device)
    model_rula.load_state_dict(torch.load(os.path.join('.', 'weights', 'rula.pth'), map_location=torch.device('cpu')))
    pose_estimation = pose_detector(os.path.join(".", "weights", "pose_coco.pth"))

    pygame.mixer.init()
    alert_sound = pygame.mixer.Sound("audio_file.mp3")

    # Page title
    # st.markdown("Real-time RULA Analysis with Webcam")
    st.markdown("<div class='section-title'>Real-time Posture risk analysis</div>", unsafe_allow_html=True)

    # Create a two-column layout
    col1, col2 = st.columns(2)

    with col1:
        col3, col4 = st.columns(2)
        with col3:
            start_button = st.button("Start Analysis")
        with col4:
            stop_button = st.button("Stop Analysis")

        # Display the webcam video feed
        video_capture = cv2.VideoCapture(0)
        video_element = st.empty()

    with col2:
        # Create space for displaying RULA Scores
        st.header("RULA Scores")
        scores_container = st.empty()

    # Analysis loop
    analysis_running = False
    scores = []

    while video_capture.isOpened():
        if start_button:
            analysis_running = True
            scores = []
            alert_playing = False

        if analysis_running:
            _, frame = video_capture.read()
            image_width = 640  # Adjust this value as needed
            image_height = int(image_width * 3 / 4)

            frame = cv2.resize(frame, (image_width, image_height))

            # Pose detection
            candidate, subset = pose_estimation(frame)

            if len(subset) < 1:
                st.warning("No poses detected in the webcam feed.")
            else:
                al_list = []
                for i in range(len(subset)):
                    if subset[i][8] == -1 or subset[i][11] == -1:
                        st.warning(f"The {i + 1}th person has missing points")
                        break

                    mid_x1 = candidate[subset[i][8].astype(int)][0]
                    mid_x2 = candidate[subset[i][11].astype(int)][0]
                    mid_y1 = candidate[subset[i][8].astype(int)][1]
                    mid_y2 = candidate[subset[i][11].astype(int)][1]
                    mid_x = (mid_x1 + mid_x2) / 2
                    mid_y = (mid_y1 + mid_y2) / 2

                    pose_xy = -1 * np.ones((18, 2))
                    for jj in range(18):
                        if subset[i][jj] > -1:
                            pose_xy[jj][:] = candidate[subset[i][jj].astype(int)][:2]
                            pose_xy[jj][0] -= mid_x
                            pose_xy[jj][1] -= mid_y
                    pose_xy = pose_xy.reshape((1, 36))
                    y_pred = model_rula(torch.tensor(pose_xy).float().to(device))

                    # Predicted action level
                    y_pred = torch.argmax(y_pred)
                    al_list.append(y_pred.item())

                scores.append(al_list)

                # Draw annotations directly on the frame
                for i in range(len(subset)):
                    if al_list:
                        cv2.putText(frame, f"Person {i + 1}: Level {al_list[i] + 1}", (10, 30 + 30 * i), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                        if al_list[i] + 1 > 2 and not alert_playing:
                            alert_sound.play()
                            alert_playing = True

                        elif al_list[i] + 1 <= 2 and alert_playing:
                            pygame.mixer.stop()
                            alert_playing = False

            # Display the resized frame with annotations and clear the previous image
            video_element.image(frame, channels="BGR", use_column_width=True, output_format="BGR")

        if stop_button:
            analysis_running = False
            alert_playing = False
            break



    # Display scores for each person when analysis is stopped
    if scores:
        scores_container.write("RULA Scores:")
        for i, score in enumerate(scores):
            scores_container.write(f"Person {i + 1}: {score}")

    # Release the webcam
    video_capture.release()
    pygame.quit()

def ImageAnalysis():
    # Initialize the model and pose detector
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model_rula = model.NN_base().to(device)
    model_rula.load_state_dict(torch.load(os.path.join('.', 'weights', 'rula.pth'), map_location=torch.device('cpu')))
    pose_estimation = pose_detector(os.path.join(".", "weights", "pose_coco.pth"))

    st.title("RULA Analysis Streamlit App")
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        img = cv2.imdecode(np.fromstring(uploaded_image.read(), np.uint8), 1)

        # Pose detection
        candidate, subset = pose_estimation(img)

        if len(subset) < 1:
            st.write("No poses detected in the uploaded image.")
        else:
            al_list = []
            for i in range(len(subset)):
                if subset[i][8] == -1 or subset[i][11] == -1:
                    st.write(f"The {i + 1}th person has missing points")
                    break
                mid_x1 = candidate[subset[i][8].astype(int)][0]
                mid_x2 = candidate[subset[i][11].astype(int)][0]
                mid_y1 = candidate[subset[i][8].astype(int)][1]
                mid_y2 = candidate[subset[i][11].astype(int)][1]
                mid_x = (mid_x1 + mid_x2) / 2
                mid_y = (mid_y1 + mid_y2) / 2

                pose_xy = -1 * np.ones((18, 2))
                for jj in range(18):
                    if subset[i][jj] > -1:
                        pose_xy[jj][:] = candidate[subset[i][jj].astype(int)][:2]
                        pose_xy[jj][0] -= mid_x
                        pose_xy[jj][1] -= mid_y
                pose_xy = pose_xy.reshape((1, 36))
                y_pred = model_rula(torch.tensor(pose_xy).float().to(device))

                # Predicted action level
                y_pred = torch.argmax(y_pred)
                al_list.append(y_pred.item())
                st.write(f"Action level of the {i + 1}th person: {y_pred.item() + 1}")

            # Display the image with results
            img = util.pose_vis(img, candidate, subset, al_list)
            st.image(img, channels="BGR")




Home,General_Guidlines, Real_Time_Monitor, Image_Analysis, Report=st.tabs(["Home","General_Guidlines", "Real Time Monitor", "Image Analysis", "Report"])

with Home:
    home()
with Real_Time_Monitor:
    RealTimeMonitor()
with  Image_Analysis:
    ImageAnalysis()
# with Report:
#     report()
pages_folder = "pages"
py_files = [f for f in os.listdir(pages_folder) if f.endswith(".py")]

selected_tab = st.tabs(
    [page[:-3] for page in py_files]
    
)

# Main content area based on selected tab
if selected_tab:
    load_page(selected_tab)
