import os
from bs4 import BeautifulSoup

# Path to the folder with HTML reports
report_folder = "test-reports"

# Loop through each file in the folder
for filename in os.listdir(report_folder):
    if filename.endswith(".html"):
        file_path = os.path.join(report_folder, filename)
        with open(file_path, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")
            print(f"\n📄 Report: {filename}")

            # ✅ Extract Start Time
            start_time_tag = soup.find("span", class_="panel-lead suite-started-time")
            start_time = start_time_tag.text.strip() if start_time_tag else "N/A"
            print(f"⏱ Start Time: {start_time}")

            # ✅ Extract End Time
            end_time_tag = soup.find("span", class_="panel-lead suite-ended-time")
            end_time = end_time_tag.text.strip() if end_time_tag else "N/A"
            print(f"⏱ End Time:   {end_time}")

            # ✅ Extract Scenario Names (optional if needed)
            scenario_tags = soup.find_all("div", class_="test-name")
            if scenario_tags:
                print("✅ Scenario Names:")
                for i, tag in enumerate(scenario_tags, 1):
                    print(f"  {i}. {tag.text.strip()}")
            else:
                print("⚠️ No scenario names found.")