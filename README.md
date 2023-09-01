# Sign-Language-Recognition-System
online website to make communication possible between normal and impaired people.
# Sign Language Recognition Application

This is a Sign Language Recognition application built using Streamlit and MediaPipe. It offers the following functionality:

## About the App
This section provides an overview of the application and its purpose.

- **Sign Language Recognition**: The application is designed to recognize sign language gestures and convert them into text or display sign language gestures corresponding to entered text.

## Usage Modes

### 1. About App
In this mode, you can learn more about the application's purpose and functionality.

### 2. Sign Language to Text
This mode allows you to use your webcam to perform sign language gestures, which are then converted into text on the screen.

### 3. Text to Sign Language
This mode enables you to enter text, and the system will display the corresponding Indian Sign Language gestures.

## Installation and Running the App

To run this application, follow these steps:

1. Install the required libraries:
   ```bash
   pip install streamlit mediapipe opencv-python-headless numpy Pillow
   ```

2. Clone the repository containing this code.

3. Navigate to the directory containing the code.

4. Run the Streamlit app:
   ```bash
   streamlit run your_file.py
   ```

Replace `your_file.py` with the name of the Python script containing this code.

## Using the Application

### About App
- Click on "About App" in the sidebar to learn about the application's purpose and functionality.

### Sign Language to Text
- Choose "Sign Language to Text" from the dropdown in the sidebar.
- Your webcam will be activated, and you can start making sign language gestures.
- The application will attempt to recognize the gestures and display the corresponding text on the screen.

### Text to Sign Language
- Choose "Text to Sign Language" from the dropdown in the sidebar.
- Enter the text you want to convert to Indian Sign Language.
- The application will display the corresponding sign language gestures for the entered text.

## Note
- The application recognizes a set of sign language gestures, such as A, B, C, etc., and converts them to text in "Sign Language to Text" mode.
- In "Text to Sign Language" mode, it displays images of Indian Sign Language gestures corresponding to the entered text.

This application aims to bridge communication gaps and promote inclusivity by making sign language more accessible.
