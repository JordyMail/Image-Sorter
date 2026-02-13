# Image-Sorter

Image-sorter is a desktop application designed to streamline the process of organizing large volumes of photos. It allows users to quickly categorize images into specific folders using customizable keyboard shortcuts.

---

## Installation

Ensure you have Python installed on your system. You can then install the necessary dependencies using pip:

```bash
pip install customtkinter pillow

```

---

## Usage Guide

1. **Run the application**:
Execute the script using the following command:
```bash
python main.py

```


2. **Setup Phase**:
* Click **Select Source Folder** to load your images.
* Click **Add New Category** to define where images should be sent.
* In the **Keyboard Shortcut** section, enter a key and check the boxes for the corresponding destination folders.


3. **Sorting Phase**:
* Click **START SORTING** to enter the viewer mode.
* The application will display the first image. Press your pre-defined shortcut keys to copy the image to your chosen folders.
* The app automatically moves to the next image after a shortcut is pressed.


4. **Completion**:
* Once all images in the folder are processed, a summary screen will appear.

