from playwright.sync_api import sync_playwright
from pathlib import Path
from datetime import datetime

# ==========================================================
# Configuration
# ==========================================================

now = datetime.now()
current_date = now.strftime("%Y-%m-%d")
current_datetime = now.strftime("%Y-%m-%d %H:%M:%S")

downloads = Path.home() / "Downloads"

report_path = downloads / f"daily_report_{current_date}.txt"
screenshot_path = downloads / f"daily_report_{current_date}.png"

url = "https://www.josalukkasonline.com/gold-rate-today/Coimbatore"

print("=" * 50)
print("Starting Playwright Daily Report Bot")
print("=" * 50)

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False
    )

    page = browser.new_page()

    page.goto(
        url,
        wait_until="networkidle"
    )

    page.wait_for_timeout(3000)

    cards = page.locator(".carat-card")

    gold_rates = []

    count = cards.count()

    for i in range(count):

        karat = cards.nth(i).locator(".karat").inner_text().strip()

        price = cards.nth(i).locator(".amount").inner_text().strip()

        gold_rates.append(f"{karat}: {price}")

    report = f"""
====================================================

DAILY GOLD RATE REPORT

====================================================

Date & Time:
{current_datetime}

----------------------------------------------------

Today's Gold Rates (Coimbatore)

----------------------------------------------------

{chr(10).join(gold_rates)}

----------------------------------------------------

Comment

----------------------------------------------------

Today's gold rates captured automatically using
Playwright automation.

====================================================
"""

    # Save report
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)

    # Save screenshot
    page.screenshot(
        path=str(screenshot_path),
        full_page=True
    )

    print()
    print("Report saved:")
    print(report_path)

    print()
    print("Screenshot saved:")
    print(screenshot_path)

    browser.close()

print()
print("=" * 50)
print("Automation Completed Successfully!")
print("=" * 50)