import time
import random
import cv2
import numpy as np
import pyautogui
from detector import search_and_click, click_use_button_relative_to_item

# Enable PyAutoGUI fail-safe
pyautogui.FAILSAFE = True

farming_steps = [
    {"step": 1, "name": "Next", "file": "images/next_button.png"},
    {"step": 2, "name": "Next", "file": "images/next_button.png"},
    {"step": 3, "name": "Next", "file": "images/next_button.png"},
    {"step": 4, "name": "Start", "file": "images/start_button.png"},
    {"step": 5, "name": "Start", "file": "images/start_button.png"},
    {"step": 6, "name": "Skip", "file": "images/skip_button.png"},
    {"step": 7, "name": "Confirm", "file": "images/confirm_button.png"},
    {"step": 8, "name": "Confirm", "file": "images/confirm_button.png"},
    {"step": 9, "name": "Close", "file": "images/close_button.png"},
    {"step": 10, "name": "Autoplay", "file": "images/autoplay_button.png"},
    {
        "step": 11,
        "name": "Start (Long Farming Phase)",
        "file": "images/start_button.png",
    },
    {
        "step": 12,
        "name": "Complete",
        "file": "images/complete_btn.png",
    },  
    {"step": 13, "name": "Finish", "file": "images/finish_button.png"},
    {"step": 14, "name": "Next", "file": "images/next_button.png"},
    {"step": 15, "name": "Decide", "file": "images/decide_button.png"},
    {"step": 16, "name": "Confirm", "file": "images/confirm_button.png"},
    {"step": 17, "name": "Close", "file": "images/close_button.png"},
    {"step": 18, "name": "Next", "file": "images/next_button.png"},
    {"step": 19, "name": "Next", "file": "images/next_button.png"},
    {"step": 20, "name": "Next", "file": "images/next_button.png"},
]


def human_delay(min_sec=1.5, max_sec=3.0):
    """Provide a random delay between steps to mimic human actions."""
    time.sleep(random.uniform(min_sec, max_sec))


def handle_tp_refill():
    """Function to handle energy depletion with priority on Toughness 30 bottles,
    then Jewels (including Plus and OK buttons) as a fallback.
    """
    print("\n[Info] Energy depleted detected. Opening Refill TP menu...")
    
    print("[Info] Clicking the Refill button...")
    while not search_and_click("images/refill_button.png", confidence_threshold=0.80):
        time.sleep(1.0)
    
    print("[Info] Waiting for the Refill TP items window to fully open...")
    human_delay(3.0, 4.0)
    
    print("[Info] Looking for Toughness 30 item...")
    success_toughness = False
    start_search_time = time.time()
    
    while not success_toughness:
        success_toughness = click_use_button_relative_to_item("images/use_toughness_button.png", x_distance_to_use=-60, confidence_threshold=0.80)
        
        if success_toughness:
            break
            
        if time.time() - start_search_time > 8.0:
            print("[Warning] Toughness 30 search timeout! Assuming it's depleted.")
            break
            
        print("[Waiting] Toughness 30 not found yet, retrying...")
        time.sleep(1.0)
    
    if success_toughness:
        print("[Success] Toughness 30 bottle used successfully!")
        print("[Info] Confirming usage (OK)...")
        while not search_and_click("images/ok_button.png", confidence_threshold=0.80):
            time.sleep(1.0)
            
    else:
        print("[Warning] Toughness 30 bottles depleted! Switching to Jewels...")
        
        jewels_search_start = time.time()
        success_jewels = False
        
        while not success_jewels:
            success_jewels = click_use_button_relative_to_item("images/use_jewels_button.png", x_distance_to_use=-60, confidence_threshold=0.80)
            
            if success_jewels:
                break
                
            if time.time() - jewels_search_start > 12.0:
                print("[CRITICAL WARNING] Jewels item box search timeout!")
                raise SystemExit
                
            print("[Waiting] Searching for Jewels item box...")
            time.sleep(1.0)
            
        print("[Success] Jewels 'Use' button clicked!")
        human_delay(1.5, 2.0)

        print("[Info] Clicking plus (+) button for Jewels...")
        while not search_and_click("images/plus_button.png", confidence_threshold=0.80):
            time.sleep(1.0)
            
        human_delay(1.0, 1.5)

        print("[Info] Confirming Jewels exchange (OK)...")
        while not search_and_click("images/ok_button.png", confidence_threshold=0.80):
            time.sleep(1.0)

    human_delay(2.0, 2.5)

    print("[Info] Closing refill window...")
    while not search_and_click("images/close_button.png", confidence_threshold=0.80):
        time.sleep(1.0)
        
    print("[Info] TP Refill completed successfully. Energy is now full!")
    human_delay(2.0, 3.0)


def run_farming_cycle():
    print("\n=== STARTING NEW FARMING CYCLE ===")

    refilled_in_this_cycle = False

    # Jalankan step 1 sampai 20 secara normal via loop
    for item in farming_steps:
        step_num = item["step"]
        action_name = item["name"]
        image_file = item["file"]

        print(f"\n[Waiting] Step {step_num}: Looking for '{action_name}'...")

        success = False
        step_start_time = time.time()
        timeout_limit = 30 * 60  # Maximum timeout limit 30 minutes per step

        while not success:
            elapsed_total = time.time() - step_start_time
            if elapsed_total >= timeout_limit:
                print(f"\n[CRITICAL WARNING] Step {step_num} ({action_name}) stuck for more than 30 minutes!")
                print("[Info] Program terminated automatically.")
                raise SystemExit

            current_threshold = 0.80

            # 1. Cari dan klik tombol step normal
            success = search_and_click(image_file, confidence_threshold=current_threshold)

            # 2. PENGAMANAN REFILL HANYA PADA SAAT KLIK 'START'
            if success and action_name == "Start" and not refilled_in_this_cycle:
                print(f"[Info] '{action_name}' clicked. Checking if energy is depleted...")
                time.sleep(2.0)  
                
                screenshot = pyautogui.screenshot()
                scr_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
                refill_template = cv2.imread("images/refill_button.png")
                
                is_actually_depleted = False
                if refill_template is not None:
                    res = cv2.matchTemplate(scr_cv, refill_template, cv2.TM_CCOEFF_NORMED)
                    _, max_v, _, _ = cv2.minMaxLoc(res)
                    
                    if max_v >= 0.95:
                        is_actually_depleted = True

                if is_actually_depleted:
                    print(f"\n[Alert] Energy depleted popup CONFIRMED! Triggering Refill workflow...")
                    handle_tp_refill()
                    refilled_in_this_cycle = True
                    
                    print(f"[Info] Refill done. Restarting current step...")
                    step_start_time = time.time()
                    success = False
                    continue
                else:
                    print(f"[Info] Energy is sufficient. Moving forward!")

            # 3. SABAR MENUNGGU DENGAN TIMER PROGRES
            if not success:
                if step_num == 11 or step_num == 12:  
                    elapsed_minutes = elapsed_total / 60
                    print(
                        f"[Farming in Progress] Waiting for process/button... Elapsed time: {elapsed_minutes:.1f}/30.0 mins",
                        end="\r",
                    )
                    time.sleep(random.uniform(5.0, 8.0))  
                else:
                    time.sleep(random.uniform(1.0, 2.0))  

        print(f" -> [Success] Step {step_num} ({action_name}) executed!")
        human_delay(1.5, 3.0)  

    # ==========================================
    #   PERCABANGAN AKHIR (DENGAN TIMEOUT 10 DETIK)
    # ==========================================
    print("\n[Info] Step 20 selesai. Memeriksa keberadaan tombol 'Try Again'...")
    time.sleep(2.0)

    try_again_clicked = False
    
    # 1. Coba cari 'Try Again' sampai 3 kali percobaan
    for attempt in range(1, 4):
        print(f"[Percobaan Try Again {attempt}/3] Mencari tombol 'Try Again'...")
        found_try_again = search_and_click("images/try_again_button.png", confidence_threshold=0.80)
        
        if found_try_again:
            print(f" -> [Success] Tombol 'Try Again' ditemukan & diklik pada percobaan ke-{attempt}!")
            try_again_clicked = True
            break
        else:
            time.sleep(1.5)

    # 2. Jika 'Try Again' tidak ketemu sama sekali setelah 3x percobaan
    if not try_again_clicked:
        print("[Info] Tombol 'Try Again' tidak ada setelah 3x percobaan. Mencari tombol 'Close' (timeout 10 detik)...")
        
        close_clicked = False
        close_start_time = time.time()
        
        while time.time() - close_start_time < 10.0:
            found_close = search_and_click("images/close_button.png", confidence_threshold=0.80)
            if found_close:
                print(" -> [Success] Tombol 'Close' pertama ditemukan & diklik!")
                close_clicked = True
                break
            time.sleep(1.0)

        if not close_clicked:
            print("[Warning] Tombol 'Close' tidak ketemu dalam 10 detik! Langsung loncat ke pencarian 3x Next...")
        else:
            time.sleep(2.0)

        # 3. Melanjutkan mencari tombol 'Next' sebanyak 3 kali berturut-turut
        print("[Info] Melanjutkan mencari tombol 'Next' sebanyak 3 kali...")
        for i in range(1, 4):
            print(f"Mencari tombol Next ke-{i}...")
            while not search_and_click("images/next_button.png", confidence_threshold=0.80):
                time.sleep(1.0)
            print(f" -> [Success] Tombol Next ke-{i} berhasil diklik.")
            time.sleep(1.5)

        # 4. Mencari tombol 'Try Again' setelah 3x Next
        print("[Info] Mencari tombol 'Try Again' setelah 3x Next...")
        while not search_and_click("images/try_again_button.png", confidence_threshold=0.80):
            time.sleep(1.0)
        print(" -> [Success] Tombol 'Try Again' berhasil diklik!")
        
        time.sleep(2.0)

    # 5. SETELAH TRY AGAIN BERHASIL DIKLIK: Cek apakah ada tombol 'Close' tambahan (timeout 10 detik)
    print("[Info] Memeriksa apakah ada tombol 'Close' setelah Try Again (timeout 10 detik)...")
    final_close_clicked = False
    final_close_start = time.time()
    
    while time.time() - final_close_start < 10.0:
        found_final_close = search_and_click("images/close_button.png", confidence_threshold=0.80)
        if found_final_close:
            print(" -> [Success] Tombol 'Close' tambahan ditemukan & diklik!")
            final_close_clicked = True
            break
        time.sleep(1.0)

    if not final_close_clicked:
        print("[Info] Tidak ada tombol 'Close' tambahan dalam 10 detik (aman). Siklus selesai, kembali ke awal!")
    else:
        print("[Info] Tombol 'Close' tambahan sudah di-klik. Siklus selesai, kembali ke awal!")


if __name__ == "__main__":
    print("=== GAME AUTOMATION PROGRAM STARTED ===")
    print("Press Ctrl+C in terminal or move mouse to screen corner for emergency stop.")
    time.sleep(2)

    try:
        cycle_count = 1
        while True:
            print(f"\n==========================================")
            print(f"            FARMING CYCLE #{cycle_count}          ")
            print(f"==========================================")

            run_farming_cycle()

            print(
                f"\nCycle #{cycle_count} completed! Preparing to restart from the beginning..."
            )
            cycle_count += 1
            human_delay(4.0, 7.0)  

    except KeyboardInterrupt:
        print("\n[Info] Program stopped manually by user.")