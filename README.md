# Image-Sorter

Image-sorter is a desktop application designed to streamline the process of organizing large volumes of photos. It allows users to quickly categorize images into specific folders using customizable keyboard shortcuts.

---

## Technical Stack

The application is built using the following tools and libraries:

* **Python 3.x**: Core programming language.
* **CustomTkinter**: For the modern, responsive graphical user interface.
* **Pillow (PIL)**: For image processing and displaying previews.
* **OS & Shutil**: For file system management and file copying operations.
* **Tkinter**: For native system dialogs and message alerts.

---

## Key Functions

* **Source Folder Selection**: Choose the directory containing the images to be organized.
* **Category Management**: Create multiple destination labels and map them to specific directory paths.
* **Keyboard Mapping**: Link specific keys (e.g., 'A', 'S', 'D') to one or more destination categories.
* **Live Image Preview**: View images with automatic aspect ratio scaling before sorting.
* **Batch Copying**: Pressing a shortcut key copies the current image to all assigned folders simultaneously.
* **Navigation Control**: Manual "Next" and "Previous" buttons to skip or review images.

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

