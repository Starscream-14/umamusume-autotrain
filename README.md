# Umamusume Automation Farming Fans

A Python-based computer vision automation designed to handle repetitive farming loops in games (such as *Umamusume*). It utilizes **OpenCV** for Template Matching and **PyAutoGUI** for automated navigation, featuring a structured data-driven workflow, long-phase waiting handlers, and continuous cycling.

---

## Project Structure

```text
umamusume-automation/
│
├── images/                 <-- Folder containing all button screenshots/templates
│   ├── next_button.png
│   ├── start_button.png
│   ├── skip_button.png
│   ├── confirm_button.png
│   ├── close_button.png
│   ├── autoplay_button.png
│   ├── complete_btn.png
│   ├── finish_button.png
│   ├── decide_button.png
│   └── try_again_button.png
│
├── detector.py             <-- Core module for OpenCV Template Matching and clicking
├── automation.py           <-- Main script containing the workflow and looping logic
└── requirements.txt        <-- Required Python packages list