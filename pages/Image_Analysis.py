import streamlit as st
# import cv2
import matplotlib.pyplot as plt
import copy
import numpy as np
import torch
from utils import model
from utils import util
from utils.pose import pose_detector
import os
from PIL import Image

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
                margin-top:  -80px; 
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
def ImageAnalysis():
    # Initialize the model and pose detector
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model_rula = model.NN_base().to(device)
    model_rula.load_state_dict(torch.load(os.path.join('.', 'weights', 'rula.pth'), map_location=torch.device('cpu')))
    # pose_estimation = pose_detector(os.path.join(".", "weights", "pose_coco.pth"))
    pose_coco_path = st.file_uploader("Upload pose_coco.pth", type=["pth"])
    if pose_coco_path is not None:
        pose_estimation = pose_detector(pose_coco_path)
        st.subheader("Image analysis based on rula score")
        uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
        if uploaded_image is not None:
            col1, col2 = st.columns(2)
            # with col1:
            # img = cv2.imdecode(np.fromstring(uploaded_image.read(), np.uint8), 1)
            img = Image.open(uploaded_image).convert("RGB")
            img = np.array(img)
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
ImageAnalysis()