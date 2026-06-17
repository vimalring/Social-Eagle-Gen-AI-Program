import pyautogui
import pyperclip
import re
import time
from pathlib import Path
from datetime import datetime

# ==========================================================
# Configuration
# ==========================================================

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5

# Current date/time
now = datetime.now()
current_date = now.strftime("%Y-%m-%d")
current_datetime = now.strftime("%Y-%m-%d %H:%M:%S")

# Downloads directory
DOWNLOADS_DIR = Path.home() / "Downloads"

# Output files
report_filename = f"daily_report_{current_date}.txt"
screenshot_filename = f"daily_report_{current_date}.png"

# Save paths
report_path = DOWNLOADS_DIR / report_filename
screenshot_path = DOWNLOADS_DIR / screenshot_filename

print("=" * 50)
print("Starting Daily Report Bot...")
print("=" * 50)

# ==========================================================
# STEP 1 - Open Chrome using Spotlight
# ==========================================================

pyautogui.hotkey("command", "space")
time.sleep(1)

pyautogui.write("Google Chrome", interval=0.05)
pyautogui.press("enter")

print("Opening Chrome...")
time.sleep(1)

# ==========================================================
# STEP 2 - Open New Tab
# ==========================================================

pyautogui.hotkey("command", "t")
time.sleep(1)

# ==========================================================
# STEP 3 - Open Website
# ==========================================================

# Type the URL like a human
pyautogui.write(
    "https://www.josalukkasonline.com/gold-rate-today/Coimbatore",
    interval=0.03  # Increase to 0.05 or 0.1 for slower typing
)

# Press Enter
pyautogui.press("enter")

print("Loading website...")
time.sleep(5)  # Increase if the page loads slowly

# ==========================================================
# STEP 4 - Select All & Copy
# ==========================================================

print("Copying webpage text...")

pyautogui.hotkey("command", "a")
time.sleep(1)

pyautogui.hotkey("command", "c")
time.sleep(2)

page_text = pyperclip.paste()

# ==========================================================
# STEP 5 - Extract Gold Rates
# ==========================================================

pattern = (
    r"24K\s*Gold.*?₹[\d,]+.*?"
    r"22K\s*Gold.*?₹[\d,]+.*?"
    r"18K\s*Gold.*?₹[\d,]+"
)

match = re.search(
    pattern,
    page_text,
    flags=re.IGNORECASE | re.DOTALL
)

if match:
    gold_rates = match.group(0)

    gold_rates = re.sub(r"\s+", " ", gold_rates)

    gold_rates = gold_rates.replace(
        "22K Gold",
        "\n22K Gold"
    )

    gold_rates = gold_rates.replace(
        "18K Gold",
        "\n18K Gold"
    )
else:
    gold_rates = "Gold rates could not be extracted."

# ==========================================================
# STEP 6 - Create Report
# ==========================================================

report = f"""
====================================================

        DAILY GOLD RATE REPORT

====================================================

Date & Time:
{current_datetime}

----------------------------------------------------

Today's Gold Rates (Coimbatore)

----------------------------------------------------

{gold_rates}

----------------------------------------------------

Comment

----------------------------------------------------

Today's gold rates captured automatically using
PyAutoGUI automation.

====================================================
"""

# ==========================================================
# STEP 7 - Open Sublime Text
# ==========================================================

pyautogui.hotkey("command", "space")
time.sleep(1)

pyautogui.write("Sublime Text", interval=0.05)
pyautogui.press("enter")

print("Opening Sublime Text...")
time.sleep(3)
# ==========================================================
# STEP 8 - Paste Report into Sublime & Save to Downloads
# ==========================================================

# Copy report to clipboard
pyperclip.copy(report)

# Paste into Sublime
pyautogui.hotkey("command", "v")
time.sleep(1)

# Open Save dialog
pyautogui.hotkey("command", "s")
time.sleep(2)

# Type the full path to the Downloads folder
# report_path is already defined as:
# DOWNLOADS_DIR / report_filename

pyperclip.copy(str(report_path))
pyautogui.hotkey("command", "v")
time.sleep(1)

# Press Enter to save
pyautogui.press("enter")
time.sleep(2)

# If a confirmation dialog appears asking to replace an existing file,
# press Enter again.
pyautogui.press("enter")
time.sleep(1)

print("Sublime file saved successfully:")
print(report_path)

# ==========================================================
# STEP 9 - Take Screenshot
# ==========================================================

image = pyautogui.screenshot()
image.save(str(screenshot_path))

print("Screenshot saved successfully:")
print(screenshot_path)

# ==========================================================
# DONE
# ==========================================================

print()
print("=" * 50)
print("Automation Completed Successfully!")
print("=" * 50)
print("Report File    :", report_path)
print("Screenshot File:", screenshot_path)