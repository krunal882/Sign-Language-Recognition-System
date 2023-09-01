import streamlit as st
import mediapipe as mp
import cv2
import numpy as np
import time
from PIL import Image
import os

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

my_list = []

st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 350px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 350px;
        margin-left: -350px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.sidebar.title("Sign Language Recognition")
st.sidebar.subheader("-Options")

@st.cache_resource()
def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image

    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)

    else:
        r = width / float(w)
        dim = (width, int(h * r))

    resized = cv2.resize(image, dim, interpolation=inter)

    return resized

app_mode = st.sidebar.selectbox(
    "Choose the App mode",
    ["About App", "Sign Language to Text", "Text to sign Language"],
)

if app_mode == "About App":
    st.title("Sign Language Recognition")
    st.markdown(
        """Welcome to our sign language recognition system! We are dedicated to breaking communication barriers and providing inclusive solutions for individuals who use sign languages.\n
        \n We believe that everyone should have equal access to communication, regardless of their preferred language modality. Our sign language recognition system aims to bridge the gap between sign language users and the wider community, enabling smoother interactions and fostering understanding."""
    )
    st.markdown(
        """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 400px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 400px;
        margin-left: -400px;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
              # About \n 
              In this application we are using **MediaPipe** for detecting Sign Language.**StreamLit** is to create the Web Graphical User Interface (GUI)\n
                
                """
    )
elif app_mode == "Sign Language to Text":
    st.title("Sign Language to Text")
    st.set_option("deprecation.showfileUploaderEncoding", False)

    out = ""
    st.markdown(" ## Output")
    st.markdown(out)

    stframe = st.empty()

    vid = cv2.VideoCapture(0)

    st.markdown("<hr/>", unsafe_allow_html=True)

    st.sidebar.markdown("---")
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
            width: 400px;
        }
        [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
            width: 400px;
            margin-left: -400px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    finger_tips = [8, 12, 16, 20]
    thumb_tip = 4
    while True:
        ret, img = vid.read()
        img = cv2.flip(img, 1)
        h, w, c = img.shape
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img)

        img.flags.writeable = True
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmark in results.multi_hand_landmarks:
                lm_list = []
                for id, lm in enumerate(hand_landmark.landmark):
                    lm_list.append(lm)
                finger_fold_status = []
                for tip in finger_tips:
                    x, y = int(lm_list[tip].x * w), int(lm_list[tip].y * h)

                    if lm_list[tip].x < lm_list[tip - 2].x:
                        finger_fold_status.append(True)
                    else:
                        finger_fold_status.append(False)

                print(finger_fold_status)
                x, y = int(lm_list[8].x * w), int(lm_list[8].y * h)
                print(x, y)

                # A
                if (
                    lm_list[2].y > lm_list[4].y
                    and lm_list[8].y > lm_list[6].y
                    and lm_list[12].y > lm_list[10].y
                    and lm_list[16].y > lm_list[14].y
                    and lm_list[20].y > lm_list[18].y
                    and lm_list[17].x < lm_list[0].x < lm_list[5].x
                    and lm_list[4].y < lm_list[6].y
                ):
                    cv2.putText(
                        img, "A", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3
                    )
                    my_list.append("A")

                # B
                if (
                    lm_list[2].x > lm_list[4].x
                    and lm_list[8].y < lm_list[6].y
                    and lm_list[12].y < lm_list[10].y
                    and lm_list[16].y < lm_list[14].y
                    and lm_list[20].y < lm_list[18].y
                    and lm_list[2].x > lm_list[8].x
                ):
                    cv2.putText(
                        img, "B", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3
                    )
                    my_list.append("B")

                # C
                if (
                    lm_list[2].x < lm_list[4].x
                    and lm_list[8].x > lm_list[6].x
                    and lm_list[12].x > lm_list[10].x
                    and lm_list[16].x > lm_list[14].x
                    and lm_list[20].x > lm_list[18].x
                    and not lm_list[4].y < lm_list[8].y
                ):
                    cv2.putText(
                        img, "C", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3
                    )
                    my_list.append("C")

                # D
                if (
                    lm_list[3].y > lm_list[4].y
                    and lm_list[8].y < lm_list[6].y
                    and lm_list[12].y > lm_list[10].y
                    and lm_list[16].y > lm_list[14].y
                    and lm_list[4].y < lm_list[12].y
                    and not lm_list[3].x > lm_list[12].x
                ):
                    cv2.putText(
                        img, "D", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3
                    )
                    my_list.append("D")

                # E
                if (
                    lm_list[2].x > lm_list[4].x
                    and lm_list[8].y > lm_list[6].y
                    and lm_list[12].y > lm_list[10].y
                    and lm_list[16].y > lm_list[14].y
                    and lm_list[20].y > lm_list[18].y
                    and lm_list[4].y > lm_list[14].y
                    and lm_list[4].y < lm_list[1].y
                    and lm_list[4].x > lm_list[16].x
                ):
                    cv2.putText(
                        img, "E", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3
                    )
                    my_list.append("E")

                # F
                if (
                    lm_list[2].y > lm_list[4].y
                    and lm_list[8].y > lm_list[6].y
                    and lm_list[12].y < lm_list[10].y
                    and lm_list[16].y < lm_list[14].y
                    and lm_list[20].y < lm_list[18].y
                    and lm_list[17].x < lm_list[0].x < lm_list[5].x
                    and lm_list[4].y > lm_list[5].y
                ):
                    cv2.putText(
                        img, "F", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3
                    )
                    my_list.append("F")

                # G
                if (
                    lm_list[2].x > lm_list[4].x
                    and lm_list[8].x < lm_list[6].x
                    and lm_list[12].x > lm_list[10].x
                    and lm_list[16].x > lm_list[14].x
                    and lm_list[20].x > lm_list[18].x
                    and lm_list[4].x > lm_list[8].x
                    and lm_list[4].x < lm_list[5].x
                    and lm_list[4].y < lm_list[12].y
                    and lm_list[4].y < lm_list[20].y
                ):
                    cv2.putText(
                        img, "G", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3
                    )
                    my_list.append("G")

                # H
                if (
                    lm_list[2].x > lm_list[4].x
                    and lm_list[8].x < lm_list[6].x
                    and lm_list[12].x < lm_list[10].x
                    and lm_list[16].x > lm_list[14].x
                    and lm_list[20].x > lm_list[18].x
                    and lm_list[4].x > lm_list[6].x
                ):
                    cv2.putText(
                        img, "H", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3
                    )
                    my_list.append("H")

                # I
                if (
                    lm_list[2].y > lm_list[4].y
                    and lm_list[8].y > lm_list[6].y
                    and lm_list[12].y > lm_list[10].y
                    and lm_list[16].y > lm_list[14].y
                    and lm_list[20].y < lm_list[18].y
                    and lm_list[6].y < lm_list[4].y
                ):
                    cv2.putText(
                        img, "I", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3
                    )
                    my_list.append("I")

                # K
                if (
                    lm_list[2].y > lm_list[4].y
                    and lm_list[8].y < lm_list[6].y
                    and lm_list[12].x < lm_list[10].x
                    and lm_list[16].y > lm_list[14].y
                    and lm_list[20].y > lm_list[18].y
                    and lm_list[4].y > lm_list[8].y
                    and lm_list[4].y > lm_list[11].y
                    and lm_list[4].y > lm_list[7].y
                    and lm_list[4].y < lm_list[5].y
                ):
                    cv2.putText(
                        img, "K", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3
                    )
                    my_list.append("K")

                # L
                if (
                    lm_list[2].x < lm_list[4].x
                    and lm_list[8].y < lm_list[6].y
                    and lm_list[12].y > lm_list[10].y
                    and lm_list[16].y > lm_list[14].y
                    and lm_list[20].y > lm_list[18].y
                    and lm_list[4].y > lm_list[6].y
                ):
                    cv2.putText(
                        img, "L", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3
                    )
                    my_list.append("L")

                # M
                if (
                    lm_list[2].x > lm_list[4].x
                    and lm_list[8].y > lm_list[6].y
                    and lm_list[12].y > lm_list[10].y
                    and lm_list[16].y > lm_list[14].y
                    and lm_list[20].y > lm_list[18].y
                    and lm_list[20].y > lm_list[8].y
                    and lm_list[20].y > lm_list[4].y
                ):
                    cv2.putText(
                        img, "M", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3
                    )
                    my_list.append("M")

                # N
                if (
                    lm_list[2].x > lm_list[4].x
                    and lm_list[8].y > lm_list[6].y
                    and lm_list[12].y > lm_list[10].y
                    and lm_list[16].y > lm_list[14].y
                    and lm_list[20].y > lm_list[18].y
                    and lm_list[16].y > lm_list[12].y
                    and lm_list[4].y < lm_list[14].y
                ):
                    cv2.putText(
                        img, "N", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3
                    )
                    my_list.append("N")

                # O
                if (
                    lm_list[3].x < lm_list[1].x
                    and lm_list[4].y > lm_list[8].y
                    and lm_list[8].y > lm_list[6].y
                    and lm_list[12].y > lm_list[10].y
                    and lm_list[16].y > lm_list[14].y
                    and lm_list[20].y > lm_list[18].y
                    and lm_list[17].x > lm_list[20].x
                ):
                    cv2.putText(
                        img, "O", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3
                    )
                    my_list.append("O")

                # P
                if (
                    lm_list[2].x > lm_list[4].x
                    and lm_list[8].x < lm_list[6].x
                    and lm_list[12].y > lm_list[10].y
                    and lm_list[15].y > lm_list[14].y
                    and lm_list[19].y > lm_list[18].y
                    and lm_list[5].x > lm_list[6].x
                ):
                    cv2.putText(
                        img, "P", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3
                    )
                    my_list.append("P")

                # Q
                if (
                    lm_list[2].y < lm_list[4].y
                    and lm_list[8].y > lm_list[6].y
                    and lm_list[12].x > lm_list[10].x
                    and lm_list[16].x > lm_list[14].x
                    and lm_list[20].x > lm_list[18].x
                    and lm_list[4].y > lm_list[6].y
                ):
                    cv2.putText(
                        img, "Q", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3
                    )
                    my_list.append("Q")

                # R
                if (
                    lm_list[2].x > lm_list[4].x
                    and lm_list[8].y < lm_list[6].y
                    and lm_list[12].y < lm_list[10].y
                    and lm_list[16].x > lm_list[14].x
                    and lm_list[20].x > lm_list[18].x
                    and lm_list[7].y > lm_list[11].y
                    and lm_list[8].x < lm_list[12].x
                    and lm_list[20].y > lm_list[16].y
                ):
                    cv2.putText(
                        img, "R", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3
                    )
                    my_list.append("R")

                # # S
                # if (
                #     lm_list[2].y > lm_list[4].y
                #     and lm_list[8].y > lm_list[6].y
                #     and lm_list[12].y > lm_list[10].y
                #     and lm_list[16].y > lm_list[14].y
                #     and lm_list[20].y > lm_list[18].y
                #     # and lm_list[16].x > lm_list[20].x
                #     # and lm_list[4].y > lm_list[6].y
                #     and lm_list[4].x < lm_list[6].x
                # ):
                #     cv2.putText(
                #         img, "S", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3
                #     )
                #     my_list.append("S")

                # T
                if (
                    lm_list[1].x > lm_list[3].x
                    and lm_list[8].x < lm_list[6].x
                    and lm_list[12].x > lm_list[10].x
                    and lm_list[16].x > lm_list[14].x
                    and lm_list[20].x > lm_list[18].x
                    and lm_list[4].x > lm_list[6].x
                    and lm_list[4].y < lm_list[12].y
                    and lm_list[4].y < lm_list[16].y
                ):
                    cv2.putText(
                        img,
                        "T",
                        (20, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 255),
                        3,
                    )
                    my_list.append("T")

                # U
                if (
                    lm_list[2].y > lm_list[4].y
                    and lm_list[4].y < lm_list[5].y
                    and lm_list[12].y < lm_list[10].y
                    and lm_list[16].x > lm_list[14].x
                    and lm_list[20].x > lm_list[18].x
                    and lm_list[6].y > lm_list[10].y
                ):
                    cv2.putText(
                        img, "U", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3
                    )
                    my_list.append("U")

                # V
                if (
                    lm_list[2].x > lm_list[4].x
                    and lm_list[8].y < lm_list[6].y
                    and lm_list[12].y < lm_list[10].y
                    and lm_list[16].y > lm_list[14].y
                    and lm_list[20].y > lm_list[18].y
                    and lm_list[8].x > lm_list[12].x
                    and not lm_list[4].y < lm_list[5].y
                ):
                    cv2.putText(
                        img, "V", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3
                    )
                    my_list.append("V")

                # W
                if (
                    lm_list[2].x > lm_list[4].x
                    and lm_list[8].y < lm_list[6].y
                    and lm_list[12].y < lm_list[10].y
                    and lm_list[16].y < lm_list[14].y
                    and lm_list[20].y > lm_list[18].y
                ):
                    cv2.putText(
                        img, "W", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3
                    )
                    my_list.append("W")

                # X
                if (
                    lm_list[2].x > lm_list[4].x
                    and lm_list[8].x < lm_list[6].x
                    and lm_list[8].y < lm_list[5].y
                    and lm_list[12].x > lm_list[10].x
                    and lm_list[16].x > lm_list[14].x
                    and lm_list[20].x > lm_list[18].x
                    and lm_list[2].x > lm_list[8].x
                    and lm_list[6].x > lm_list[10].x
                    and lm_list[5].x > lm_list[10].x
                ):
                    cv2.putText(
                        img, "X", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3
                    )
                    my_list.append("X")

                # Y
                if (
                    lm_list[2].y > lm_list[4].y
                    and lm_list[8].y > lm_list[6].y
                    and lm_list[12].y > lm_list[10].y
                    and lm_list[16].y > lm_list[14].y
                    and lm_list[20].y < lm_list[18].y
                    and lm_list[14].y > lm_list[20].y
                    and lm_list[6].y > lm_list[4].y
                ):
                    cv2.putText(
                        img, "Y", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3
                    )
                    my_list.append("Y")

            mp_draw.draw_landmarks(
                img,
                hand_landmark,
                mp_hands.HAND_CONNECTIONS,
                mp_draw.DrawingSpec((0, 0, 255), 6, 3),
                mp_draw.DrawingSpec((0, 255, 0), 4, 2),
            )

            frame = cv2.resize(img, (0, 0), fx=0.8, fy=0.8)
            frame = image_resize(image=frame, width=640)
            stframe.image(frame, channels="BGR", use_column_width=True)

else:
    st.title("Text to Sign Language (The System use Indian Sign Language)")

    def display_images(text):
        img_dir = "images/"

        image_pos = st.empty()

        for char in text:
            if char.isalpha():
                img_path = os.path.join(img_dir, f"{char}.png")
                img = Image.open(img_path)

                image_pos.image(img, width=500)

                time.sleep(1)

                image_pos.empty()
            elif char == " ":
                img_path = os.path.join(img_dir, "space.png")
                img = Image.open(img_path)

                image_pos.image(img, width=500)

                time.sleep(1)

                image_pos.empty()

        time.sleep(2)
        image_pos.empty()

    text = st.text_input("Enter text:")
    text = text.lower()

    display_images(text)


