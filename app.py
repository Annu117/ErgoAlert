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
from PIL import Image

# Set Streamlit page configuration
st.set_page_config(
    page_title="ErgoAlert",
    page_icon="E_logo1.png",
    layout="wide"
)
custom_css = """
        <style>
            body {
                    font-family: 'Arial', sans-serif;
                    background-color: #f5f5f5;
                }
            .main {
                margin-left: -80px;
                padding: 20px;
                margin-top:  -110px; 
            }
            .section-title {
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 20px;
        }
        </style>
    """
st.markdown(custom_css, unsafe_allow_html=True)

st.markdown('<link rel="stylesheet" type="text/css" href="styles.css">', unsafe_allow_html=True)
def load_page(pages):
    page_module = __import__(f"pages.{pages[:-3]}", fromlist=["main"])
    page_module.main()
def home():
    st.header("Ergonomic Risk Analysis")
    st.write(
        "Welcome to the Ergonomic Risk Analysis, a real-time solution for assessing and mitigating ergonomic risks during work. "
        "Utilizing computer vision and the RULA scoring method, this website provides actionable insights and alerts to enhance workplace safety."
    )

    st.image("image (2).png", use_column_width=True, caption="Ergonomic Workspace")

    st.markdown("<div class='section-title'>Key Features and Benefits</div>", unsafe_allow_html=True)
    st.write(
        "- **Real-time Ergonomic Analysis:** Continuously monitor and analyze users' postures in real-time using computer vision.\n"
        "- **Ergonomic Suggestions:** Receive personalized ergonomic advice based on RULA scores, promoting better posture and reducing risks.\n"
        "- **Alert System:** Instant notifications for supervisors or workers when extended periods of harmful postures are detected.\n"
        # "- **Data Insights:** Access comprehensive data insights to identify trends and areas for improvement.\n"
        # "- **User-Friendly Interface:** Easy-to-use interface for a seamless experience."
    )

    st.markdown("<div class='section-title'>Get Started</div>", unsafe_allow_html=True)
    st.write(
        "To begin using the Ergonomic Risk Analysis, follow these steps:\n"
        "1. **Start Analysis:** Click the 'Start Analysis' button to initiate real-time posture monitoring.\n"
        "2. **Receive Scores:** Get RULA scores along with ergonomic suggestions displayed in the interface.\n"
        "3. **Alerts and Recommendations:** Receive alerts for prolonged harmful postures and follow ergonomic recommendations.\n"
        "4. **Enhance Workplace Safety:** Implement suggested changes to improve the overall ergonomic environment."
    )

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
    st.markdown("---")
    st.markdown("<div class='section-title'>Position for Safety and Comfort</div>", unsafe_allow_html=True)

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

    st.markdown("<div class='section-title'>Remember</div>", unsafe_allow_html=True)
    remember_points = [
        "WHEN KEYING, float your hands over the keyboard, and use palm rests between bursts of keying.",
        "WHEN MOUSING, keep your wrists straight, and use the elbow to pivot.",
        "ADJUST your chair to fit you, if possible.",
        "CHANGE your working position often throughout the day, stretching your fingers, hands, arms, and torso, and by standing and walking around for a few minutes periodically."
    ]
    for point in remember_points:
        st.markdown(f" - {point}")
    st.markdown("---")
def report():
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
def yoga_pose(description, instructions, image_path):
    col1, col2 = st.columns([1, 2])  # Adjusted column width proportions
    with col1:
        st.image(image_path, use_column_width=True)
    with col2:
        st.markdown(f"<div class='section-title' ;> {description}</div>\n\n{instructions}", unsafe_allow_html=True)
def yoga_sequence():
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

def RealTimeMonitor():
    st.markdown('<link rel="stylesheet" type="text/css" href="styles.css">', unsafe_allow_html=True)

    start_time = 0
    end_time = 0
    # Initialize the model and pose detector
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model_rula = model.NN_base().to(device)
    model_rula.load_state_dict(torch.load(os.path.join('.', 'weights', 'rula.pth'), map_location=torch.device('cpu')))
    pose_estimation = pose_detector(os.path.join(".", "weights", "pose_coco.pth"))

    pygame.mixer.init()
    alert_sound = pygame.mixer.Sound("audio_file.mp3")
    st.markdown("<div class='section-title'>Real-time Posture risk analysis</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        col3, col4 = st.columns(2)
        with col3:
            start_button = st.button("Start Analysis")
        with col4:
            stop_button = st.button("Stop Analysis")  

    with col2:
        video_capture = cv2.VideoCapture(0)
        video_element = st.empty()

    # Analysis loop
    analysis_running = False
    analysis_started = False
    scores = []
    level_counts = {"Level 1": 0, "Level 2": 0, "Level 3": 0, "Level 4": 0}

    while video_capture.isOpened():
        if start_button and not stop_button:
            analysis_running = True
            analysis_started = True
            scores = []
            alert_playing = False
            start_time = time.time()
            
        if analysis_running and not stop_button:
            _, frame = video_capture.read()
            image_width = 640  
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
                        # # st.warning(f"The {i + 1}th person has missing points")
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

                # Draw annotations directly on the frame
                for i in range(len(subset)):
                    if i < len(al_list):
                        if al_list:
                            cv2.putText(frame, f"Person {i + 1}: Level {al_list[i] + 1}", (10, 30 + 30 * i), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 1255), 2)
                            print(al_list[i] + 1)
                            if al_list[i] + 1 == 1:
                                level_counts["Level 1"] += 1
                            elif al_list[i] + 1 == 2:
                                level_counts["Level 2"] += 1
                                print("Level 2: " + str(level_counts["Level 2"]))
                            elif al_list[i] + 1 == 3:
                                level_counts["Level 3"] += 1
                                print("Level 3: " + str(level_counts["Level 3"]))

                            elif al_list[i] + 1 == 4:
                                level_counts["Level 4"] += 1
                            # level_counts[f"Level {al_list[i] + 1}"] += 1
                            if al_list[i] + 1 > 2 and not alert_playing:
                                alert_sound.play()
                                alert_playing = True

                            elif al_list[i] + 1 <= 2 and alert_playing:
                                pygame.mixer.stop()
                                alert_playing = False

            # Display the resized frame with annotations and clear the previous image
            video_element.image(frame, channels="BGR", use_column_width=True, output_format="BGR")

        if stop_button :
            analysis_running = False
            alert_playing = False
            end_time = time.time()
            st.write(scores)
            
            print(level_counts)
            for key, value in level_counts.items():
                st.write(f'{key}: {value}')

            break

    video_capture.release()
    pygame.quit()
    total_time = end_time - start_time

def ImageAnalysis():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model_rula = model.NN_base().to(device)
    model_rula.load_state_dict(torch.load(os.path.join('.', 'weights', 'rula.pth'), map_location=torch.device('cpu')))
    pose_estimation = pose_detector(os.path.join(".", "weights", "pose_coco.pth"))

    st.subheader("Image analysis based on rula score")
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        col1, col2 = st.columns(2)
        # with col1:
        img = cv2.imdecode(np.fromstring(uploaded_image.read(), np.uint8), 1)

        # Pose detection
        candidate, subset = pose_estimation(img)

        if len(subset) < 1:
            st.write("No poses detected in the uploaded image.")
        else:
            al_list = []
            with col2:
                st.write("**Risk Level**")
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
                with col2:

                    st.write(f" {i + 1}th person: {y_pred.item() + 1}")
            with col1:
                # Display the image with results
                img = util.pose_vis(img, candidate, subset, al_list)
                st.image(img, channels="BGR")

    

Home,General_Guidlines, Image_Analysis, Report, Yoga_Poses,Real_Time_Monitor,=st.tabs(["Home","General Guidlines", "Image Analysis", "Report", "Yoga Sequence", "Real Time Monitor"])

with Home:
    home()
with General_Guidlines:
    general_guidline()
# with Real_Time_Monitor:
#     RealTimeMonitor()
with Image_Analysis:
    ImageAnalysis()
with Report:
    report()
with Yoga_Poses:
    yoga_sequence()
# pages_folder = "pages"
# py_files = [f for f in os.listdir(pages_folder) if f.endswith(".py")]

# selected_tab = st.tabs(
#     [page[:-3] for page in py_files]
    
# )

# # Main content area based on selected tab
# if selected_tab:
#     load_page(selected_tab)
