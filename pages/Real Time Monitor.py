# import streamlit as st
# import cv2
# import numpy as np
# import torch
# from utils import model
# from utils.pose import pose_detector
# import os
# import pygame
# import time
# st.set_page_config(
#     page_title="Real-time Risk Monitor",
#     page_icon="E_logo1.png",
#     layout="wide"
# )
# level_counts = {"Level 1": 0, "Level 2": 0, "Level 3": 0, "Level 4": 0}

# custom_css = """
#         <style>
#             body {
#                     font-family: 'Arial', sans-serif;
#                     background-color: #f5f5f5;
#                 }
#             .main {
#                 margin-left: -70px;
#                 padding: 20px;
#                 margin-top:  -110px; 
#             }
#             .section-title {
#             font-size: 17px;
#             font-weight: bold;
#             margin-bottom: 20px;
#         }
#         </style>
#     """

# st.markdown(custom_css, unsafe_allow_html=True)
# st.markdown('<link rel="stylesheet" type="text/css" href="styles.css">', unsafe_allow_html=True)
# def RealTimeMonitor():
#     global level_counts
#     start_time = 0
#     end_time = 0
#     # Initialize the model and pose detector
#     device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#     model_rula = model.NN_base().to(device)
#     model_rula.load_state_dict(torch.load(os.path.join('.', 'weights', 'rula.pth'), map_location=torch.device('cpu')))
#     pose_estimation = pose_detector(os.path.join(".", "weights", "pose_coco.pth"))

#     pygame.mixer.init()
#     alert_sound = pygame.mixer.Sound("audio_file.mp3")
#     st.subheader("Real-time Posture risk analysis")
#         # Analysis loop
#     analysis_running = False
#     analysis_started = False
#     scores = []
#     col1, col2 = st.columns(2)
#     with col1:
#         col3, col4 = st.columns(2)
#         with col3:
#             start_button = st.button("Start Analysis")
#         with col4:
#             stop_button = st.button("Stop Analysis")  
#     with col2:
#         video_capture = cv2.VideoCapture(0)
#         video_element = st.empty()
#         alert_enabled = st.checkbox("Enable Alert Indication", value=True)

#     while video_capture.isOpened():
#         if start_button and not stop_button:
#             analysis_running = True
#             analysis_started = True
#             scores = []
#             alert_playing = False
#             start_time = time.time()
            
#         if analysis_running and not stop_button:
#             _, frame = video_capture.read()
#             image_width = 640  
#             image_height = int(image_width * 3 / 4)

#             frame = cv2.resize(frame, (image_width, image_height))

#             # Pose detection
#             candidate, subset = pose_estimation(frame)

#             if len(subset) < 1:
#                 st.warning("No poses detected in the webcam feed.")
#             else:
#                 al_list = []
#                 for i in range(len(subset)):
#                     if subset[i][8] == -1 or subset[i][11] == -1:
#                         # # st.warning(f"The {i + 1}th person has missing points")
#                         break
#                     mid_x1 = candidate[subset[i][8].astype(int)][0]
#                     mid_x2 = candidate[subset[i][11].astype(int)][0]
#                     mid_y1 = candidate[subset[i][8].astype(int)][1]
#                     mid_y2 = candidate[subset[i][11].astype(int)][1]
#                     mid_x = (mid_x1 + mid_x2) / 2
#                     mid_y = (mid_y1 + mid_y2) / 2

#                     pose_xy = -1 * np.ones((18, 2))
#                     for jj in range(18):
#                         if subset[i][jj] > -1:
#                             pose_xy[jj][:] = candidate[subset[i][jj].astype(int)][:2]
#                             pose_xy[jj][0] -= mid_x
#                             pose_xy[jj][1] -= mid_y
#                     pose_xy = pose_xy.reshape((1, 36))
#                     y_pred = model_rula(torch.tensor(pose_xy).float().to(device))

#                     # Predicted action level
#                     y_pred = torch.argmax(y_pred)
#                     al_list.append(y_pred.item())

#                 # Draw annotations directly on the frame
#                 for i in range(len(subset)):
#                     if i < len(al_list):
#                         if al_list:
#                             cv2.putText(frame, f"Person {i + 1}: Level {al_list[i] + 1}", (10, 30 + 30 * i), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 1255), 2)
#                             print(al_list[i] + 1)
#                             if al_list[i] + 1 == 1:
#                                 level_counts["Level 1"] += 1
#                             elif al_list[i] + 1 == 2:
#                                 level_counts["Level 2"] += 1
#                                 print("Level 2: " + str(level_counts["Level 2"]))
#                             elif al_list[i] + 1 == 3:
#                                 level_counts["Level 3"] += 1
#                                 print("Level 3: " + str(level_counts["Level 3"]))

#                             elif al_list[i] + 1 == 4:
#                                 level_counts["Level 4"] += 1
#                             # level_counts[f"Level {al_list[i] + 1}"] += 1
#                             if al_list[i] + 1 > 2 and not alert_playing and alert_enabled:
#                                 alert_sound.play()
#                                 alert_playing = True

#                             elif al_list[i] + 1 <= 2 and alert_playing and alert_playing:
#                                 pygame.mixer.stop()
#                                 alert_playing = False

#             # Display the resized frame with annotations and clear the previous image
#             video_element.image(frame, channels="BGR", use_column_width=True, output_format="BGR")

#         elif stop_button :
#             analysis_running = False
#             alert_playing = False
#             end_time = time.time()
#             st.markdown("<div class='section-title'>Report</div>", unsafe_allow_html=True)
#             # st.write("Report")
#             print(level_counts)
#             for key, value in level_counts.items():
#                 st.write(f'{key}: {value}')

#             break

#     video_capture.release()
#     pygame.quit()
#     total_time = end_time - start_time

# RealTimeMonitor()