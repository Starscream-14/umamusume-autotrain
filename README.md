# Umamusume Automation Farming Fans

A Python-based computer vision automation designed to handle repetitive farming loops in Umamusume: Pretty Derby. It utilizes **OpenCV** for Template Matching and **PyAutoGUI** for automated navigation, featuring a structured data-driven workflow, long-phase waiting handlers, and continuous cycling.

---

## Project Structure

```text
├── images/
│   ├── autoplay_button.png
│   ├── close_button.png
│   ├── complete_btn.png
│   ├── confirm_button.png
│   ├── decide_button.png
│   ├── finish_button.png
│   ├── next_button.png
│   ├── ok_button.png
│   ├── plus_button.png
│   ├── refill_button.png
│   ├── skip_button.png
│   ├── start_button.png
│   ├── try_again_button.png
│   ├── use_jewels_button.png
│   └── use_toughness_button.png
│
├── automation.py          
├── automation_event.py    
├── detector.py            
├── README.md
└── requirements.txt
```

---

## Requirements

1. Make sure Python is installed on your system.
2. Install the required dependencies:
```
pip install -r requirements.txt
```

## How To Use

Run the main automation script from your terminal:
```
python automation.py
```
Or
```
python automation_event.py
```

## Notes
1. Only works on Umamusume Japanese Version with English Translated and URA Finale Scenario.
