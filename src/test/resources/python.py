import os
from bs4 import BeautifulSoup

# Folder where ExtentReport HTML files are stored
report_folder = "test-reports"

# Loop through each HTML file in the folder
for filename in os.listdir(report_folder):
    if filename.endswith(".html"):
        file_path = os.path.join(report_folder, filename)
        with open(file_path, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")
            print(f"\n🔍 Parsing report: {filename}")

            # ✅ 1. Extract Start and End Time
            time_info = soup.find("div", class_="time-info")  # Adjust if class name differs
            if time_info:
                spans = time_info.find_all("span")
                if len(spans) >= 4:
                    start_time = spans[1].text.strip()
                    end_time = spans[3].text.strip()
                    print(f"⏱ Start Time: {start_time}")
                    print(f"⏱ End Time:   {end_time}")
                else:
                    print("⚠️ Start/End time not found.")
            else:
                print("⚠️ 'time-info' section missing.")

            # ✅ 2. Extract Scenario/Test Names
            test_names = soup.find_all("div", class_="test-name")  # Adjust class if needed
            if test_names:
                print("✅ Scenario Names:")
                for i, name in enumerate(test_names, 1):
                    print(f"  {i}. {name.text.strip()}")
            else:
                print("⚠️ No scenarios found.")