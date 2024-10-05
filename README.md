# Python Keylogger
This project is a Python-based keylogger that captures keystrokes, monitors clipboard activity, and takes periodic screenshots. It logs everything into text files and sends the logs to an email address.Please ensure you are using it in a lawful manner and within ethical boundaries.

# Key Features
Keystroke Logging: Records every key pressed on the keyboard
Clipboard Monitoring: Tracks any text copied to the clipboard.
Active Window Logging: Logs the title of the currently active window.
Screenshot Capture: Takes screenshots at regular intervals.
Email Reporting: Sends captured logs to your designated email.
Log Compression: Compresses log files to save space and make sending easier.
Optional Self-Destruction: The script can delete itself after it finishes running.

# Requirements
Python 3.x
Install these Python libraries if you haven't already(using pip):
keyboard
pygetwindow
pyperclip
Pillow (for screenshots)
smtplib (for email)
gzip and shutil (for compression)
threading (for multitasking)

# Before running this codeS
Set up environment variables for EMAIL_ADDRESS,EMAIL_PASSWORD,RECEIVER_EMAIL;
Set up LOG_DIR as the path of the directory where you want to store your keystroke captures;

# Legal use
Do not use this tool without permission on any system. Unauthorized use of keyloggers is illegal and unethical.

